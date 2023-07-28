# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    width = fields.Float('Width', digits='Standard Dimension')
    height = fields.Float('Height', digits='Standard Dimension')
    depth = fields.Float('Depth', digits='Standard Dimension')
    standard_dimension_id = fields.Many2one("standard.dimension", string="Standard Dimension")