# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Delivery Shipping Information ",
    "summary": "To Know delivery Shipping Information",
    "author": "",
    "website": "",
    "category": "Sale",
    "version": "14.0.1.0",

    "license": "AGPL-3",

    "depends": ["base", "sale_management", "purchase", "hallmark"],
    'data': [
        'views/sale_order_custom_views.xml',
        'views/purchase_order_custom_views.xml',
        'views/stock_picking_views.xml',
        'views/sale_report_custom_views.xml',
        # 'views/purchase_report_custom_views.xml',
    ],
    "demo": [],
    'installable': True,
    'auto_install': False,
    'application': True,

}
