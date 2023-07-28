# -*- coding: utf-8 -*-
from odoo import fields, models, api

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    children_info_id = fields.One2many('children', 'children_id','Children Information')
    resume_file = fields.Binary("Resume")
    file_name = fields.Char("File Name")

class Children(models.Model):
    _name = 'children'

    children_id = fields.Many2one("hr.employee","Children")
    name = fields.Char("Name")
    birthday = fields.Date("Birthday")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')

