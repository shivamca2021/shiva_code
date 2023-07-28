# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_id = fields.Char("Customer ID")
    customer_code = fields.Char('Customer Code')

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence']
        vals['customer_id'] = seq.next_by_code(
            'dfm.contact') or '/'
        res = super(ResPartner, self).create(vals)
        return res