{
	"name": "Prism",
	"version": "14.0",
	"author": "IC-KPI",
	"website": "http://www.ic-kpi.com",
	"sequence": 5,
	"depends": [
		"base","hr","hr_skills","sale","hr_maintenance","sales_team"
	],
	"category": "Settings",
	"complexity": "easy",
	"description": """	
	""",
	"data": [
		"security/ir.model.access.csv",
		"views/commission_view.xml",
		"views/employee_view.xml",
		"views/maintenance_view.xml",
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