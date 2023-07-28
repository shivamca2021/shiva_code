# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    installation_date = fields.Date('Installation Date')
