from odoo import models, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime


class Sale(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """inherit for check partner due amount"""
        if self.partner_id.credit_limit > 0.0:
            if self.currency_id == self.env.company.currency_id:
                if self.partner_id.credit_limit < (self.partner_id.total_due + self.amount_total):
                    raise ValidationError(_('Amount due show up only when we have the some '
                                            'dues available, in the from of some invoices in validated state'))
            else:
                currency_rate = self.env['res.currency']._get_conversion_rate(self.env.company.currency_id,
                                                                              self.currency_id, self.company_id,
                                                                              self.date_order)
                if not currency_rate:
                    raise ValidationError(_('Currency Rate is not found'))
                if self.partner_id.credit_limit < (self.partner_id.total_due + (self.amount_total * currency_rate)):
                    raise ValidationError(_('Amount due show up only when we have the some '
                                            'dues available, in the from of some invoices in validated state'))
        res = super(Sale, self).action_confirm()
        return res