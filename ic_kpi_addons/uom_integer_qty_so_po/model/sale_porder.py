from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLineInheritInteger(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom_qty')
    def _check_integer_so(self):
        for rec in self:
            if rec.product_uom.is_integer_qty:
                x = (rec.product_uom_qty % 1)
                if x != 0:
                    raise ValidationError("Please Enter Integer values Quantity Field")


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty')
    # @api.constrains('product_uom.is_integer_qty', 'product_uom_qty')
    def _check_integer_qty_po(self):
        for rec in self:
            if rec.product_uom.is_integer_qty:
                x = (rec.product_uom_qty % 1)
                if x != 0:
                    raise ValidationError("Please Enter Integer values in Quantity  Field")
