import base64
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.payment_authorize.controllers.main import AuthorizeController
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.tools import pycompat
import io
import xlrd
import logging
_logger = logging.getLogger(__name__)

class WebsiteOrder(http.Controller):

    def check_file_type_header(self, type, file, file_type):
        FILE_TYPE_DICT = [
            'text/csv',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ]

        customer_headers = ['name','company name','contact name','street','street2','city','zip','fax','mobile','email','phone' ,'state name','country name','website name','tag name']
        vendor_headers = ['name','company name','contact name','street','street2','city','zip','fax','mobile','email','phone' ,'state name','country name','website name','tag name']
        employee_headers = ['employee name', 'job position name', 'department name', 'manager name', 'work mobile', 'work phone', 'work email',
 'coach name', 'marital status', 'country name', 'identification no', 'passport no', 'gender', 'date of birth', 'place of birth',
 'country of birth', 'number of children', 'work permit no', 'visa no', 'visa expire date', 'categorys']
        msg = 's'
        if type == 'customer':
            chk_header = customer_headers
            error = 'C'
            if file_type not in FILE_TYPE_DICT:
                error = 'C_M'
                return error

        elif type == 'vendor':
            chk_header = vendor_headers
            error = 'V'
            if file_type not in FILE_TYPE_DICT:
                error = 'V_M'
                return error
        else:
            chk_header = employee_headers
            error = 'E'
            if file_type not in FILE_TYPE_DICT:
                error = 'E_M'
                return error

        if file_type == 'text/csv':
                csv_iterator = pycompat.csv_reader(
                               io.BytesIO(file),
                               quotechar='"',
                               delimiter=',')
                row = (
                        row for row in csv_iterator
                        if any(x for x in row if x.strip())
                    )
                headers = next(row, None)
                header = list(map(lambda x: x.lower(), headers))
                if chk_header != header or len(chk_header) != len(header):
                    return error
        else:
            book = xlrd.open_workbook(file_contents=file)
            sheets =  book.sheet_names()
            sheet_name =  sheets[0]
            sheet = book.sheet_by_name(sheet_name)
            headers = sheet.row_values(0)
            header = list(map(lambda x: x.lower(), headers))
            if chk_header != header  or len(chk_header) != len(header):
                return error
        return msg

    @http.route(['/website-order/customer-information'], type='http', auth="public", website=True)
    def customer_details_form(self, **kw):
        values = {
            'countries': request.env['res.country'].sudo().search([]),
            'states': request.env['res.country.state'].sudo().search([]),
        }
        return request.render("website_order.form_customer_detais", values)

    @http.route(['/website_order/customer_details_submit'], type='http', auth="public", methods=['POST'], website=True)
    def get_customer_details(self, **kw):
        if len(kw) != 0 and 'name' in kw:
            partner_id = request.env['res.partner'].sudo().create({
                'name': kw.get('name'),
                'image_1920': base64.b64encode(kw.get('uclogo').read() or b''),
                'street': kw.get('street'),
                'street2': kw.get('street2'),
                'city': kw.get('city'),
                'state_id': int(kw.get('state_id')) if kw.get('state_id',None) else '',
                'country_id': int(kw.get('country_id')) if kw.get('country_id',None) else '',
                'email': kw.get('email'),
                'mobile': kw.get('phone'),
                'create_instance': True,
                'zip':kw.get('zip') if kw.get('zip', None) else ''
            })
            return str(partner_id.id)

    @http.route(['/website-order/payment-information'], type='http', auth="public", website=True)
    def payment_form_load(self, **kwargs):
        acquirers = request.env['payment.acquirer'].search([
            ('state', 'in', ['enabled', 'test'])
            # ('registration_view_template_id', '!=', False), ('payment_flow', '=', 's2s'), ('company_id', '=', request.env.company.id)
        ])

        payment_tokens = request.env['payment.token'].sudo().search([
            ('acquirer_id', 'in', acquirers.ids), ('partner_id', '=', kwargs.get('partner_id'))])
        return_url = request.params.get('redirect', '/my/payment_method')
        values = {
            'pms': payment_tokens,
            'acquirers': acquirers,
            'error_message': [kwargs['error']] if kwargs.get('error') else False,
            'return_url': return_url,
            'bootstrap_formatting': True,
            'partner_id': kwargs.get('partner_id')
        }
        #return request.render("website_sale.payment", values)
        #return request.render("payment.pay_methods", values)

        '''values = {
            'acquirers': acquirers,
            'tokens': payment_tokens,
            'partner_id': kwargs.get('partner_id'),
        }'''
        return request.render("website_order.order_form_payment_details", values)

    @http.route(['/website_order/order_payment_form_submit'], type='http', auth="public", website=True)
    def get_payment_submit(self, **kw):
        product = request.env.ref("website_order.product_product_order_cst_product_template",raise_if_not_found=False)
        vals = {
            'partner_id': int(kw.get('partner_id')),
            'state':'sale',
        }
        if product:
            if kw.get('a_id', False):
                vals.update({'order_line': [(0, 0, {'product_id': product.product_variant_id.id, 'qty_delivered': 1})]})
            else:
                vals.update({'order_line': [(0, 0, {'product_id': product.product_variant_id.id, 'qty_delivered': 1, 'price_unit': (product.list_price + ((product.list_price * 3.5)/100)) })]})
        order = request.env['sale.order'].sudo().browse(int(kw.get('o_id'))) if kw.get('o_id', False) else request.env['sale.order'].sudo().create(vals)
        invoice_vals_list = []
        invoice_line_vals = []
        final = True
        invoice_item_sequence = 0
        invoice_vals = order._prepare_invoice()
        invoiceable_lines = order._get_invoiceable_lines(final)
        for line in invoiceable_lines:
            invoice_line_vals.append(
                (0, 0, line._prepare_invoice_line(
                    sequence=invoice_item_sequence,
                )),
            )
            invoice_item_sequence += 1
        invoice_vals['invoice_line_ids'] += invoice_line_vals
        invoice_vals_list.append(invoice_vals)
        moves = request.env['account.move'].sudo().with_context(
            default_move_type='out_invoice').create(invoice_vals_list)
        moves.action_post()
        vals = {
            'acquirer_id': int(kw.get('a_id')) if kw.get('a_id', False) else request.env.ref("payment.payment_acquirer_authorize").id,
            'payment_token_id': int(kw.get('pm_id')) if kw.get('pm_id', False) else None,
            'acquirer_reference': kw.get('t_id') if kw.get('t_id', False) else None
        }
        tx = moves._create_payment_transaction(vals)
        PaymentProcessing.add_payment_transaction(tx)
        return request.redirect('/website-order/user-information?partner_id='+ kw.get('partner_id'))

    @http.route(['/website-order/user-information'], type='http', auth="public", website=True)
    def user_details_form(self, **kw):
        values = {'partner_id': kw.get('partner_id')}
        return request.render("website_order.form_user_detais", values)

    @http.route(['/website_order/user_details_submit_form'], type='http', methods=['POST'], csrf=True, auth="public", website=True)
    def user_details_form_submit(self, **kw):
        redirect_url = {}
        if kw.get('partner_id'):
            partner_id = request.env['res.partner'].browse(int(kw.get('partner_id')))
            user_email_data = []
            user_data = []
            result = list(filter(lambda x: x.startswith('user_email_'), kw))
            for user_email in result:
                user_email_data.append(user_email.replace('user_email_', ''))
            for user in range(int(max(user_email_data))+1):
                user_info_id = request.env['user.info'].sudo().create({
                    'name': kw.get('user_name_%s' %user),
                    'email': kw.get('user_email_%s' %user),
                    'passwd': kw.get('user_pwd_%s' %user),
                    'is_admin': kw.get('is_admin_%s' %user),
                })
                user_data.append(user_info_id.id)
            c_file = kw.get('customer_file').read() or b''
            msg = self.check_file_type_header('customer',c_file,kw.get('customer_file').content_type)
            if msg != 's':
                return msg
            v_file = kw.get('vendor_file').read() or b''
            msg = self.check_file_type_header('vendor',v_file,kw.get('vendor_file').content_type)
            if msg != 's':
                return msg
            e_file = kw.get('emp_file').read() or b''
            msg = self.check_file_type_header('employee',e_file,kw.get('emp_file').content_type)
            if msg != 's':
                return msg

            partner_id.sudo().write({
                'user_info_ids': [(6, 0, user_data)],
                'customer_import': c_file,
                'customer_import_name': kw.get('customer_file').filename,
                'customer_import_file_type': kw.get('customer_file').content_type,
                'vendor_import': v_file,
                'vendor_import_name': kw.get('vendor_file').filename,
                'vendor_import_file_type': kw.get('vendor_file').content_type,
                'employee_import': e_file,
                'employee_import_name': kw.get('emp_file').filename,
                'employee_import_file_type': kw.get('emp_file').content_type,
                #'employee_import': base64.b64encode(kw.get('chat_of_acc_file').read()), chartofacc_import
                #'employee_import_name': kw.get('chat_of_acc_file').filename, chartofacc_import_name
                #'chartofacc_import_file_type': kw.get('chat_of_acc_file').content_type,
            })
        redirect_url['url'] = '/website-order/thank-you'
        return str(partner_id)

    @http.route(['/website-order/thank-you'], type='http', auth="public", website=True)
    def thank_you_page(self, **kw):
        return request.render("website_order.thank_you_page", {})

    @http.route(['/shop/country_infos/<model("res.country"):country>'], type='json', auth="public", methods=['POST'], website=True)
    def country_state_infos(self, country, **kw):
        return dict(
            fields=country.get_address_fields(),
            states=[(st.id, st.name, st.code) for st in country.sudo().state_ids],
            phone_code=country.phone_code,
            zip_required=country.zip_required,
            state_required=country.state_required,
        )

    @http.route(['/check_partner_email'], type='json', auth="public", methods=['POST'], website=True)
    def check_partner_email(self, email, **kw):
        vals = {}

        if kw.get('model') == 'user.info':
            user_info_rec = request.env['user.info'].sudo().search([('email', '=', (kw.get('email') or email))], limit=1)
            if user_info_rec:
                vals.update({'email_exist': True})
            else:
                vals.update({'email_exist': False})
            return vals

        # email validation
        if kw.get('email') and not tools.single_email_re.match(kw.get('email')):
            vals.update({
                'error': True,
                'error_msg' : 'Invalid Email! Please enter a valid email address.',
            })
            return vals

        partner_rec = request.env['res.partner'].sudo().search([('email','=', (kw.get('email') or email))], limit=1)
        if partner_rec:
            vals.update({'email_exist':True})
        else:
            vals.update({'email_exist': False})
        return vals

    @http.route(['/update/partner/bank_details'], type='json', auth="none", csrf=False, save_session=False)
    def update_partner_details(self, **kw):
        if kw.get('partner_id'):
            bank = request.env['res.bank'].sudo().search([('name','=',kw.get('bank_name'))])
            if bank:
                bank_id = bank.id
            else:
                bank = request.env['res.bank'].sudo().create({'name':kw.get('bank_name')})
                bank_id = bank.id
            partner_id = request.env['res.partner'].browse(int(kw.get('partner_id')))
            acc_numbers = partner_id.sudo().bank_ids.mapped('acc_number')
            if kw.get('account_number') not in acc_numbers:
                partner_id.sudo().bank_ids = [(0,0,
                                               {'aba_routing':kw.get('routing_number'),
                                                'acc_number':kw.get('account_number'),
                                                'acc_holder_name':kw.get('account_name'),
                                                'bank_id':bank_id
                                                })]
            payment_acquirer = request.env['payment.acquirer'].sudo().browse(int(kw.get('acquirer_id')))
            product = request.env.ref("website_order.product_product_order_cst_product_template",raise_if_not_found=False)
            vals = {
                'partner_id': int(kw.get('partner_id')),
                'state':'sale',
            }
            if product:
                vals.update({'order_line': [(0, 0, {'product_id': product.product_variant_id.id, 'qty_delivered': 1})]})
            order = request.env['sale.order'].sudo().create(vals)
            amount = round(order.amount_total, 2)
            order_line = order.order_line
            amount_tax = round(order.amount_tax, 2)
            _logger.info(amount)
            _logger.info(amount_tax)
            response = payment_acquirer.debit_bank_account(partner_id, amount, order_line, amount_tax)
            if response['messages']['resultCode'] == "Ok":
                t_id = response['transactionResponse']['transId']
                o_id = order.id
                redirect = '/website_order/order_payment_form_submit?partner_id='+ kw.get('partner_id')+'&a_id='+str(payment_acquirer.id)+'&t_id='+str(t_id)+'&o_id='+str(o_id)
            else:
                redirect = '/website-order/thank-you'
        return {'redirect_url':redirect}
