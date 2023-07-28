# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    minimum_order_quantity = fields.Float(string='Minimum Order Quantity',
                                          help="This field display minimum order qunatity")
