from odoo import models, fields, api, _


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom_qty')
    def float_round_so(self):
        for rec in self:
            if rec.product_uom.is_round_qty:
                rec.product_uom_qty = round(rec.product_uom_qty)


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty')
    def float_round_po(self):
        for rec in self:
            if rec.product_uom.is_round_qty:
                rec.product_qty = round(rec.product_qty)
