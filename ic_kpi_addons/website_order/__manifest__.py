# -*- coding: utf-8 -*-
{
    "name": "ICKPI Website Order",
    "version": "14.0.1.0.0",
    "category": "Website",
    "description": "This module is used for Website Order",
    "depends": ['sale_management', 'website', 'backend_theme_extension', 'ickpi_user_creation', 'payment_authorize'],
    "data": [
        'security/ir.model.access.csv',
        'data/payment_trasaction_update.xml',
        'views/website_template.xml',
        'views/template.xml',
        'data/product_data.xml',
        'views/order_info.xml',
        'views/assets.xml',
        # 'data/website_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
