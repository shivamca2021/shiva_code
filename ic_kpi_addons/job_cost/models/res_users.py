# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    workcenter_id = fields.Many2one('mrp.workcenter', string="Work Center")
    