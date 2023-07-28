{
    "name": "Falcon Report",
    "version": "14.0.0.1",
    "author": "IC-KPI",
    "website": "http://www.ic-kpi.com",
    "sequence": 5,
    "depends": [
        "base", "purchase", "stock",'sale'
    ],
    "category": "Settings",
    "complexity": "easy",
    "description": """	""",
    "data": [
        'report/invoice_layout.xml',
        'views/purchase_order_custom_view.xml',
        'views/account_move_custom_view.xml',
        'views/sale_order_estimate_custom_view.xml',
        'report/layout.xml',
        'report/falcon_purchase_report.xml',
        'report/sale_order_layout.xml',
        'report/falcon_sale_estimation_report.xml',
        'report/falcon_invoice_report_template.xml',
    ],

    'qweb': [],
    "auto_install": False,
    "installable": True,
    "application": False,
    'images': [],
    'license': 'LGPL-3',
}
