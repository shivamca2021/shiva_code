# -*- coding: utf-8 -*-
from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('delivery_charge','amount_untaxed')
    def _compute_amount_without_delivery(self):
        for record in self:
            if record.amount_untaxed:
                delivery = any(line.is_delivery for line in record.order_line)
                if not delivery:
                    record.delivery_charge = 0.0
                    record.delivery_details = ''
                record.amount_without_delivery = record.amount_untaxed - record.delivery_charge
            else:
                record.amount_without_delivery = 0.0

    delivery_charge = fields.Float("Delivery Charge")
    delivery_details = fields.Char("Delivery Details")
    amount_without_delivery = fields.Float(compute='_compute_amount_without_delivery', string='Amount without delivery')

    def _create_delivery_line(self, carrier, price_unit):
        order_line_vals = super(SaleOrder, self)._create_delivery_line(carrier, price_unit)
        print(order_line_vals)
        self.write({'delivery_charge':price_unit, 'delivery_details': carrier.display_name})
        return order_line_vals

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('price_unit', 'discount')
    def _compute_net_price_unit(self):
        for record in self:
            if record.price_unit or record.discount:
                record.net_price_unit = record.price_unit * (1 - (record.discount or 0.0) / 100.0)
            else:
                record.net_price_unit = record.price_unit or 0.0


    net_price_unit = fields.Float(compute='_compute_net_price_unit', string="Net Price Unit", store=True)

    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res.update({'is_delivery': self.is_delivery})
        print(res)
        return res