# -*- coding: utf-8 -*-

from odoo import models, fields

class SidebarMenu(models.Model):
    _name = 'sidebar.menu'
    _description = 'Configure Apps for Sidebar Panel'

    name = fields.Char('Sidebar menu', required=True)
    related_apps = fields.Many2many('ir.ui.menu', string='Related apps', required=True)
    sidebar_image = fields.Binary()
    right_side_image = fields.Binary()

class ResCompany(models.Model):
    _inherit = 'res.company'

    logo_image = fields.Binary()
