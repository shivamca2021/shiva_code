{
    "name": "Product Configured",
    "version": "14.0.1",
    "author": "IC-KPI",
    "website": "http://www.ic-kpi.com",
    "sequence": 5,
    "depends": [
        "base", "sale", "product", "stock", "account", "sale_product_configurator", "mrp"
    ],
    "category": "Settings",
    "complexity": "easy",
    "description": """	
	""",
    "data": [
        "data/product_configured_data.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "wizard/parts_add_view.xml",
        "wizard/product_configuration_wizard.xml",
        "views/product_configured_view.xml",
        "views/sale_order_view.xml",
        "views/product_view.xml",
        "views/stock_view.xml",
        "views/invoice_view.xml",
        "views/assets.xml",
        'views/templates.xml',
        'views/formula_variable.xml',
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
