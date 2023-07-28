# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class FavIrUiMenu(models.Model):
    _name = 'fav.menu'
    _description = 'Arc Theme Favorite Menu'

    fav_app = fields.Boolean(string='Fav App')
    users = fields.Many2one(comodel_name='res.users')
    backend_ir_ui_menu = fields.Many2one(comodel_name='ir.ui.menu')
