# -*- coding: utf-8 -*-

from pyparsing import line
from odoo import models, fields, api


class UomUom(models.Model):
    _inherit = 'uom.uom'
    
    use_int = fields.Boolean('Use Int')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty_int(self):
        if self.product_uom.use_int:
            self.product_uom_qty = int(self.product_uom_qty)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    @api.onchange('product_qty')
    def _onchange_product_qty_int(self):
        if self.product_uom.use_int:
            self.product_qty = int(self.product_qty)