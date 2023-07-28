# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    job_number = fields.Char('Job Number')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    width = fields.Char('Width')
    height = fields.Char('Height')
    depth = fields.Char('Depth')


