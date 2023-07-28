# -*- encoding: utf-8 -*-
{
	"name": "CRM Opportunity Product",
	"version": "14.0",
	"author": "IC-KPI",
	"website": "http://www.ic-kpi.com",
	"sequence": 5,
	"depends": [
		"base", 'sale_crm', 'sale', 'product','mail','calendar'
	],
	"category": "Settings",
	"complexity": "easy",
	"description": """
	This module allow to add products on opportunity and create quote with that. 
	""",
	"data": [
		'security/ir.model.access.csv',
		'views/opportunity_product.xml',
		'views/menu_item.xml',
		'views/calendar.xml',
		'views/template.xml',
		'wizard/contact_salesperson_view.xml',
	],
	"demo": [
	],
	"test": [
	],
	'qweb': [
			# "static/src/xml/template.xml",
		],
	"auto_install": False,
	"installable": True,
	"application": False,
    'images': ['static/description/banner'],
	'license': 'LGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
