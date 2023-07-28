{
    "name": "Import Orders",
    "version": "14.0",
    "author": "IC-KPI",
    "website": "http://www.ic-kpi.com",
    "sequence": 5,
    "depends": [
        "base", "sale", "sale_management"
    ],
    "category": "Settings",
    "complexity": "easy",
    "description": """	
	""",
    "data": [
        'wizard/import_order_view.xml',
        'views/sale_order_view.xml',
        'security/ir.model.access.csv'

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
