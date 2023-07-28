# -*- coding: utf-8 -*-


from odoo import api,fields,models,_
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Raise the warning "Minimum order quantity of the product <Name> is <Quantity Value>."
    # if the order quantity is less than the 'Minimum Order Quantity' of the Product.
    @api.constrains('order_line')
    def check_constraint_quantity(self):
        for record in self:
            if record.order_line:
                for product_ids in record.order_line:
                    product = product_ids.product_id.id
                    minimum_order_qty = self.env['product.product'].browse(product).minimum_order_quantity
                    if product_ids.product_uom_qty < minimum_order_qty:
                        raise ValidationError(_('Minimum order quantity of the product ' + product_ids.name+' is ' +str(minimum_order_qty)))
