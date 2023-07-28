from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'uom.uom'
    _description = 'Radio button for '

    is_integer_qty = fields.Boolean(string='Is Integer', default=False)



