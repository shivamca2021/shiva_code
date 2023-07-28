# -*- encoding: utf-8 -*-
{
	"name": "Sale Revision History",
	"version": "14.0",
	"author": "IC-KPI",
	"website": "http://www.ic-kpi.com",
	"sequence": 0,
	"depends": ["sale", "sale_stock", "sale_management"],
	"category": "Sales,Invoicing",
	"complexity": "easy",
	'license': 'LGPL-3',
	"description": """Quotation sale revision history
	""",
	"data": [
		'views/sale_order_views.xml',
		],
	"auto_install": False,
	"installable": True,
	"application": False,
	'images': ['static/description/banner.png'],

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
