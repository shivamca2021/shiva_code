{
    "name": "Apapt",
    "version": "14.0.0.1",
    "sequence": 5,
    "depends": [
        "website", "backend_theme_extension", "ickpi_prism_theme"
    ],
    "category": "Website",
    "description": """	
	""",
    "data": [
        'security/ir.model.access.csv',
        'views/assets.xml',
        #'views/template.xml',
        'data/adapt_menu.xml',
    ],
    'qweb': ["static/src/xml/apps_extend.xml"],
    "auto_install": False,
    "installable": True,
    "application": False,
    'license': 'LGPL-3',
}
