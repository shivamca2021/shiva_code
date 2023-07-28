# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models

class PrismDashboard(models.Model):
    _name = "prism.dashboard"
    _description = "Prism Dashboard"

    opportunity_name = fields.Char('Opportunity Reference')
    so_name = fields.Char('Sale Order Reference')