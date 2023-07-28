{
    "name": "Hallmark Report",
    "version": "14.0.0.1",
    "author": "IC-KPI",
    "website": "http://www.ic-kpi.com",
    "sequence": 5,
    "depends": [
        "base", "sale", "stock", "product", "delivery", "purchase_stock", "purchase","product"
    ],
    "category": "Settings",
    "complexity": "easy",
    "description": """	""",
    "data": [
        'data/cron.xml',
        # 'report/hallmark_delivery_barcode.xml',
        'report/picking_templates.xml',
        'report/layout.xml',
        'report/hallmark_report.xml',
        'report/hallmark_purchase_report.xml',
        'views/sale_order.xml',
        'views/sales_report_views.xml',
        'views/inventory.xml',
        'views/packaging.xml',
        'views/purchase.xml',
        'views/product_view.xml',
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
