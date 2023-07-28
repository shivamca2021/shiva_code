from odoo import fields,models, api, _
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Monetary('Credit Limit', tracking=True)

    @api.constrains('credit_limit')
    def credit_limit_partner(self):
        for partner in self:
            if partner.credit_limit < 0:
                raise ValidationError(_('Customer credit limit should be greater than 0'))

