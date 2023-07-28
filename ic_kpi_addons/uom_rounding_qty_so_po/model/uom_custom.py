from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'uom.uom'
    _description = 'Radio button for '

    is_round_qty = fields.Boolean(string='Round off Qty', default=False)



