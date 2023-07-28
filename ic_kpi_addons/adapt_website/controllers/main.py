# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import Controller, request, route
from werkzeug.utils import redirect
from odoo.addons.web.controllers.main import Home
import json

class Home(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        res = super(Home, self).web_client(s_action, **kw)
        sidebar_menu = request.env['sidebar.menu'].search([])
        sidebar_rec_data = request.env['ir.model.data'].sudo().search([('res_id', 'in', sidebar_menu.ids), ('model', '=', 'sidebar.menu')])
        for i in sidebar_rec_data:
            i.write({'noupdate': False})
        sidebar_rec_data = request.env['ir.model.data'].sudo().search(
            [('res_id', 'in', sidebar_menu.ids), ('model', '=', 'sidebar.menu'), ('name', '=', 'options_menu_data')], limit=1)
        # request.env['sidebar.menu'].browse(sidebar_rec_data.res_id).sudo().unlink()
        # sidebar_rec_data.unlink()
        res.qcontext.update({'sidebar_menu': sidebar_menu})
        return res