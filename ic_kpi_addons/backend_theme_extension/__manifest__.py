# -*- coding: utf-8 -*-

{
    "name": "Sidebar and Dashboard Customization",
    "summary": "Sidebar and Dashboard Customization",
    "version": "1.0",
    "category": "Theme/Backend",
    "website": "",
    "description": """ Customised sidebar and dashbiard apps.
    """,
    'images':[
	],
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'base',
        'web',
        'portal',
        'website',
        'web_responsive',
        'backend_theme_v14'
    ],
    "data": [
        'data/theme_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/sidebar.xml',
        'views/sidebar_views.xml',
        'views/website_templates.xml',
    ],
    "qweb": [
        "static/src/xml/apps_extend.xml",
        "static/src/xml/backend_appdrawer_edit.xml",
    ],
}
