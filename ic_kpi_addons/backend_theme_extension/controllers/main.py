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
        res.qcontext.update({'sidebar_menu': sidebar_menu})
        return res

    @route(['/submenu/dashboard'], type='json', auth='public', website=True)
    def dashboard_submenu(self, menu_name, **post):
        menu_ids = []
        adapt_app = request.env['ir.module.module'].search([('name', '=', 'adapt_website')], limit=1)
        related_apps = request.env['sidebar.menu'].search([('name', '=ilike', menu_name)])
        backend_all_fav_app = request.env['fav.menu'].search([
            ('users', '=', request.env.user.id)
        ])
        for menu in backend_all_fav_app:
            menu_ids.append(menu.backend_ir_ui_menu.id)
        if menu_name == 'Sales/Marketing':
            if request.env.user.has_group('backend_theme_extension.group_sale_marketing_side_bar'):
                return request.env['ir.ui.view']._render_template("backend_theme_extension.app_menu_data",
                                                                  {
                                                                      'related_apps': related_apps.related_apps._filter_visible_menus(),
                                                                      'backend_all_fav_app': backend_all_fav_app,
                                                                      'menu_ids': menu_ids,
                                                                      'sidebar_obj': related_apps,
                                                                      'adapt_state': adapt_app.state
                                                                  })
            else:
                return False
        elif menu_name == 'Purchasing/Inventory':
            if request.env.user.has_group('backend_theme_extension.group_purchasing_inventory_side_bar'):
                return request.env['ir.ui.view']._render_template("backend_theme_extension.app_menu_data",
                                                                  {
                                                                      'related_apps': related_apps.related_apps._filter_visible_menus(),
                                                                      'backend_all_fav_app': backend_all_fav_app,
                                                                      'menu_ids': menu_ids,
                                                                      'sidebar_obj': related_apps,
                                                                      'adapt_state': adapt_app.state})
            else:
                return False
        elif menu_name == 'Manufacturing/Service':
            if request.env.user.has_group('backend_theme_extension.group_manufacturing_service_side_bar'):
                return request.env['ir.ui.view']._render_template("backend_theme_extension.app_menu_data",
                                                                  {
                                                                      'related_apps': related_apps.related_apps._filter_visible_menus(),
                                                                      'backend_all_fav_app': backend_all_fav_app,
                                                                      'menu_ids': menu_ids,
                                                                      'sidebar_obj': related_apps,
                                                                      'adapt_state': adapt_app.state})
            else:
                return False

        elif menu_name == 'Accounting/HR':
            if request.env.user.has_group('backend_theme_extension.group_accounting_hr_side_bar'):
                return request.env['ir.ui.view']._render_template("backend_theme_extension.app_menu_data",
                                                                  {
                                                                      'related_apps': related_apps.related_apps._filter_visible_menus(),
                                                                      'backend_all_fav_app': backend_all_fav_app,
                                                                      'menu_ids': menu_ids,
                                                                      'sidebar_obj': related_apps,
                                                                      'adapt_state': adapt_app.state})
            else:
                return False
        elif menu_name == 'Options to Grow Your System':
            if request.env.user.has_group('backend_theme_extension.group_options_side_bar'):
                return request.env['ir.ui.view']._render_template("backend_theme_extension.app_menu_data",
                                                                  {
                                                                      'related_apps': related_apps.related_apps._filter_visible_menus(),
                                                                      'backend_all_fav_app': backend_all_fav_app,
                                                                      'menu_ids': menu_ids,
                                                                      'sidebar_obj': related_apps,
                                                                      'adapt_state': adapt_app.state})
            else:
                return False
        else:

            return False

    @http.route('/get_state', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def get_state(self, **kw):
        company = request.env.company
        data = {}
        data.update({'company_phone': company.phone, 'company_email': company.email, 'company_name': company.name
                     })
        return json.dumps(data)


class BackendThemeExtension(http.Controller):

    @route(['/backend_theme_extension/set_fav_icons'], type='json', auth='user')
    def set_fav_icons(self, backend_app_id=None):
        if backend_app_id:
            backend_app_id = int(backend_app_id)
            backend_domain = [
                ('backend_ir_ui_menu', '=', backend_app_id),
                ('users', '=', request.env.user.id)
            ]
            backend_is_fav_app = request.env['fav.menu'].search(backend_domain)
            if backend_is_fav_app:
                backend_is_fav_app.write({'fav_app': True})
                return True
            else:
                backend_is_fav_app.create(
                    {
                        'fav_app': True,
                        'backend_ir_ui_menu': backend_app_id,
                        'users': request.env.user.id
                    }
                )
                return True

    @route(['/backend_theme_extension/rmv_fav_icons'], type='json', auth='user')
    def rmv_fav_icons(self, backend_app_id=None):
        if backend_app_id:
            backend_app_id = int(backend_app_id)
            backend_domain = [
                ('backend_ir_ui_menu', '=', backend_app_id),
                ('users', '=', request.env.user.id)
            ]
            backend_is_fav_app = request.env['fav.menu'].search(backend_domain)

            if backend_is_fav_app:
                backend_is_fav_app.write({'fav_app': False})
                return True
            else:
                backend_is_fav_app.create(
                    {
                        'fav_app': False,
                        'backend_ir_ui_menu': backend_app_id,
                        'users': request.env.user.id
                    }
                )
                return True

    @route(['/backend_theme_extension/show_all_fav_icon'], type='json', auth='user')
    def show_all_fav_icon(self):
        adapt_app = request.env['ir.module.module'].search([('name', '=', 'adapt_website')], limit=1)
        backend_domain = [
            ('fav_app', '=', True),
            ('users', '=', request.env.user.id)
        ]
        backend_all_fav_app = request.env['fav.menu'].search(backend_domain)
        return request.env['ir.ui.view']._render_template("backend_theme_extension.fav_applist_bottom",
                                                          {'backend_all_fav_app': backend_all_fav_app, 'adapt_state': adapt_app.state})