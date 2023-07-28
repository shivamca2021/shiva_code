from odoo import fields, models, api


class Sale(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sale Line'

    f_d1 = fields.Selection([('f_24', '24'),
                             ('f_30', '30'),
                             ], string='D1')
    f_d2 = fields.Selection([('f_60', '60'),
                             ('f_66', '66'),
                             ('f_72', '72'),
                             ('f_84', '84')], string='D2')
    f_w1 = fields.Selection([('f_42', '42'),
                             ('f_48', '48'),
                             ('f_60', '60'),
                             ('f_66', '66'),
                             ('f_72', '72')], string='W1')
    f_w2 = fields.Selection([('f_24', '24'),
                             ('f_30', '30')], string='W2')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    id_assigned = fields.Many2one('hr.employee', 'ID Assigned')
    me_assigned = fields.Many2one('hr.employee', 'ME Assigned')
    serviced_by = fields.Many2one('hr.employee', 'Serviced By')
    probabality = fields.Selection(
        selection=[
            ('low', 'Low: 10-30%'),
            ('medium', 'Medium: 40-70%'),
            ('high', 'High : 80-100%'),
        ],
    )
    support_level = fields.Many2one('sale.support', 'Support Level')

    # sales_rep = fields.Many2one('res.partner', 'Sales Rep', domain="[('parent_id', '=', partner_id)]")
    # main_contact = fields.Many2one('res.partner','Main Contact', domain="[('parent_id', '=', partner_id)]")
    # cc_1 = fields.Many2one('res.partner','CC: (1)', domain="[('parent_id', '=', partner_id)]")
    # cc_2 = fields.Many2one('res.partner', 'CC: (2)', domain="[('parent_id', '=', partner_id)]")
    # cc_3 = fields.Many2one('res.partner', 'CC: (3)', domain="[('parent_id', '=', partner_id)]")

    template = fields.Boolean()
    vife_only = fields.Boolean('VIF Only (Site)')
    vife_only_access = fields.Boolean('VIF Only (Access)')
    delivery_vif_included = fields.Boolean('Delivery and Installation (VIF Included)')
    non_dfm_assistance = fields.Boolean('Non Dfm Installation Assistance')
    solid_surface = fields.Boolean('Stone / Solid Surface Labor')
    cut_out = fields.Boolean('Cut Out')
    chargeable_service = fields.Boolean('Chargeable Service')
    non_chargeable_service = fields.Boolean('Non Chargeable Service')
    union_labour = fields.Boolean('Union Labor')
    non_union_labour = fields.Boolean('Non-Union Labor')

    attachment_ids = fields.One2many("sale.attachments", "order_id")

    job_site_contact_name = fields.Char("Job Site Contact Name")
    email = fields.Char("Email")
    phone = fields.Char("Phone")
    shipping_method = fields.Selection([
        ('local_site', 'Local Site (Blanket Wrap)'),
        ('local_wherehouse', 'Local Wherehouse (Pallet)'),
        ('local', 'Local (Crate)'),
        ('local_glass', 'Local Glass/Stone ("A" Frame)'),
        ('state_site', 'Out of State Site (Blanket Wrap)'),
        ('state_wherehouse', 'Out of State Wherehouse (Pallet)'),
        ('state_create', 'Out of State (Crate)'),
        ('state_glass', 'Out of State Glass/Stone ("A" Frame)'),
        ],)
    site_resources = fields.Selection([
        ('union', 'Union Labor)'),
        ('non_union', 'Non-Union Labor)'),
        ],)
    internal_comments = fields.Text("Internal Comments")

    approval_contact = fields.Many2one("res.partner", string="Approval Contact", domain="[('parent_id', '=', partner_shipping_id)]")
    project_manager = fields.Many2one("res.partner", string="Project Manager", domain="[('parent_id', '=', partner_shipping_id)]")
    architect_designer = fields.Many2one("res.partner", string="Architect / Designer", domain="[('parent_id', '=', partner_shipping_id)]")
    end_user = fields.Many2one("res.partner", string="End User", domain="[('parent_id', '=', partner_shipping_id)]")
    superintendent = fields.Many2one("res.partner", string="Superintendent", domain="[('parent_id', '=', partner_shipping_id)]")
    contractor = fields.Many2one("res.partner", string="Contractor", domain="[('parent_id', '=', partner_shipping_id)]")


    alternative_gl_account = fields.Many2one("account.account")
    payment_terms = fields.Many2one("account.account","Payment Terms")
    tax_rate = fields.Many2one("account.account","Tax Rate by State")

    customer_po = fields.Char("Customer PO")
    approval_backup = fields.Char("Approval Backup")
    change_order_fee = fields.Char("Change Order Fee")
    date_of_po_entry = fields.Datetime("Date of PO Entry")
    fully_dispatched_date = fields.Datetime("Fully Dispatched Date")
    date_of_approval = fields.Datetime("Date of Approval")


    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrder, self).default_get(fields_list)
        vals = [(0, 0, {'label': "Floor Plan"}),
                (0, 0, {'label': "Electrical Plans"}),
                (0, 0, {'label': "Access  /  Elevator dimensions"}),
                (0, 0, {'label': "Reference PDF"}),
                (0, 0, {'label': "Reference Images"}),
                (0, 0, {'label': "Dfm Preliminar Drawings"}),
                (0, 0, {'label': "Dfm Sales Drawings"})]
        res.update({'attachment_ids': vals})
        return res


class SaleSupport(models.Model):
    _name = "sale.support"

    name = fields.Char('Name', required=True)


class SaleAttachments(models.Model):
    _name = "sale.attachments"

    label = fields.Char("Label")
    is_required = fields.Boolean("Is Required")
    attachments = fields.Many2many("ir.attachment")
    order_id = fields.Many2one("sale.order")
