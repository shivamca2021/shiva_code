# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Prism Dashboard',
    'version': '1.0',
    'category': 'Sales/Sales',
    'summary': '360 view of Opportunity to Manufacturing Orders',
    'description': """
This module contains 360 view of related documents from Opportunity to Manufacturing Orders.
    """,
    'depends': ['sale', 'crm', 'stock', 'purchase', 'mrp', 'account', 'sale_crm', 'sale_stock'],
    'data': [
        #'security/dashboard_security.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/prism_dashboard_view.xml',
        'views/stock_picking_view.xml',
        'report/dashboard_report_view.xml',
        'views/assets.xml',
    ],
    'demo': [

    ],
    'qweb': [
        'static/src/xml/prism_dashboard.xml',
    ],
    'installable': True,
    'auto_install': False
}
