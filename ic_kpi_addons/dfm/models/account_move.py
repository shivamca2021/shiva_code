# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_origin')
    def _compute_sale_order(self):
        for record in self:
            if record.invoice_origin:
                order_id = self.env['sale.order'].search([('name', '=', record.invoice_origin)], limit=1)
                if order_id:
                    record.sale_order_id = order_id.id
                else:
                    record.sale_order_id = False
            else:
                record.sale_order_id = False

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', compute='_compute_sale_order', store=True)



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('price_unit', 'discount')
    def _compute_invoice_net_price_unit(self):
        for record in self:
            if record.price_unit or record.discount:
                record.net_price_unit = record.price_unit * (1 - (record.discount or 0.0) / 100.0)
            else:
                record.net_price_unit = record.price_unit or 0.0

    net_price_unit = fields.Float(compute='_compute_invoice_net_price_unit', string="Net Price Unit", store=True)
    is_delivery = fields.Boolean('Is Delivery')

