from odoo import fields, models, api, _
import base64
import xlrd
import io
from datetime import datetime, date
import logging
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#
#     def import_order(self):
#         return True

class SaleImport(models.TransientModel):
    _name = 'sale.import'

    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')
    file = fields.Binary('File')
    template_id = fields.Many2one('sale.template', string="Template")
    assign = fields.Boolean(default=False)

    # @api.onchange('assign')
    # def onchange_assign(self):
    #     if self.assign:
    #         raise UserError('Please arrange the column in file based on the selected template')

    def import_sale(self):
        if self.import_option == 'csv':
            keys = []
            file_reader = []
            csv_data = base64.b64decode(self.file)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            data_file.seek(0)
            csv_reader = csv.reader(data_file, delimiter=',')
            values = {}
            value1 = {}
            list_of_column_names=[]
            file_reader.extend(csv_reader)
            for row in file_reader:
                list_of_column_names.append(row)
            column_names = list_of_column_names[0]
            sale_tmp = self.env['sale.template'].search([('id', '=', self.template_id.id)])
            for i in range(1, len(column_names)+1):
                keys.append('column'+ str(i))
            for i in range(len(file_reader)):
                field = list(map(str, file_reader[i]))
                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        j = 0
                        for line in sale_tmp.sale_template_line_ids:
                            if line.field_id.id == False:
                                j += 1
                            else:
                                j += 1
                                value1.update({line.field_id.field_description: field[j-1]})
                        res = self.create_sale_order(value1)
        else:
            try:
                workbook = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
            except:
                raise ValidationError("Please select your .xls/xlsx file.")
            sheet_name = workbook.sheet_names()
            sheet = workbook.sheet_by_name(sheet_name[0])
            sale_tmp = self.env['sale.template'].search([('id', '=', self.template_id.id)])
            value2 = {}
            nrows = sheet.nrows
            row = 1
            while (row < nrows):
                j = 0
                for line in sale_tmp.sale_template_line_ids:
                    if line.field_id.id == False:
                        j += 1
                    else:
                        j += 1
                        value2.update({line.field_id.field_description: sheet.cell(row, j-1).value})
                row = row + 1
                res = self.create_sale_order(value2)

    def create_sale_order(self, values):
        if values.get("Customer") == "":
            raise UserError(_('Customer field cannot be empty.'))
        if values.get("Product") == "":
            raise UserError(_('Product field cannot be empty.'))
        if values.get("Description") == "":
            raise UserError(_('Description field cannot be empty.'))
        if values.get("UOM") == "":
            raise UserError(_('UOM field cannot be empty.'))
        if values.get("Unit Price") == "":
            raise UserError(_('Unit Price field cannot be empty.'))
        # if values.get(line.column) == "":
        #     raise UserError(_('%s field cannot be empty.') % line.column)
        partner_id = self.find_partner(values.get('Customer'))
        today = date.today()
        dt_min = datetime.combine(today, datetime.min.time())
        dt_max = datetime.combine(today, datetime.max.time())
        orders = self.env['sale.order'].search([('partner_id', '=', partner_id.id), ('date_order', '>=', dt_min), ('date_order', '<=', dt_max)])
        if orders:
            sale_obj = orders
        else:
            sale_obj = self.env['sale.order'].create({'partner_id': partner_id.id})
        product_id = self.env['product.product'].search([('barcode', '=', values.get('Product'))])
        if product_id.id == False:
            raise UserError(_(' "%s" Product is not available.') % values.get('Product'))
        product_uom = self.env['uom.uom'].search([('name', '=', values.get('Unit of Measure'))])
        if product_uom.id == False:
            raise UserError(_(' "%s" Product UOM category is not available.') % values.get('Unit of Measure'))
        sale_line_obj = self.env['sale.order.line'].create({'product_template_id': product_id.product_tmpl_id.id,
                                                                'product_id': product_id.id,
                                                                'name': values.get("Description"),
                                                                'product_uom_qty': values.get("Quantity"),
                                                                'product_uom': product_uom.id,
                                                                'price_unit': float(values.get("Unit Price"))/int(values.get("Quantity")),
                                                                'order_id': sale_obj.id
                                                            })


    def find_partner(self, name):
        partner_obj = self.env['res.partner']
        partner_search = partner_obj.search([('name', '=', name)], limit=1)
        if partner_search:
            return partner_search
        else:
            partner_id = partner_obj.create({
                'name': name})
            return partner_id

    def find_product(self, name):
        product_obj = self.env['product.product']
        product_search = product_obj.search([('barcode', '=', name)])
        if product_search:
            return product_search
