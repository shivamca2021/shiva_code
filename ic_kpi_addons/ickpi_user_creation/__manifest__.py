{
    "name": "ICKPI User Creation",
    "version": "14.0.1",
    "author": "IC-KPI",
    "website": "http://www.ic-kpi.com",
    "sequence": 5,
    "depends": [
        "base", "contacts",
    ],
    "category": "Settings",
    "complexity": "easy",
    "description": """	
	""",
    "data": [
            'security/ir.model.access.csv',
            'data/cron.xml',
            'views/user.xml'
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
