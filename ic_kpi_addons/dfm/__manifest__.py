{
	"name": "DFM",
	"version": "14.0",
	"author": "IC-KPI",
	"website": "http://www.ic-kpi.com",
	"sequence": 5,
	"depends": [
		"base", "sale", "sale_management", "account","hr","hr_skills","purchase"
	],
	"category": "Settings",
	"complexity": "easy",
	"description": """	
	""",
	"data": [
		'data/dfm_data.xml',
		'report/dfm_report.xml',
		'report/layout.xml',
		'report/dfm_report_template.xml',
		'report/dfm_invoice_report.xml',
		'report/dfm_purchase_report.xml',
		'report/dfm_quotation_report.xml',
		'views/template.xml',
		'views/res_partner_view.xml',
		'views/account_move_view.xml',
		'views/sale_order.xml',
	],
	"demo": [
	],
	"test": [
	],
	'qweb': [],
	"auto_install": False,
	"installable": True,
	"application": False,
    'images': ['static/description/banner'],
	'license': 'LGPL-3',
}