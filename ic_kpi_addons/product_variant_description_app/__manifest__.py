# -*- coding: utf-8 -*-

{
    'name': 'Product Variant Description',
    'author': 'Edge Technologies',
    'version': '14.0.1.1',
    'live_test_url': "https://youtu.be/m73AH7pDC8s",
    'images':['static/description/main_screenshot.png'],
    'summary': 'Sales product variants description sale product variant description purchase product variant description for sales delivery product variant description for picking invoice product variants description sales order product variants description for purchase',
    'license':'OPL-1',
    'description': """
        This app helps you to set description for each of the variant of same product.
        By default odoo does not allow to separate each product variant description,
        main product description copied to all variant related to same product.
    """,
    'depends': ['sale_management','purchase','stock','sale_product_configurator'],
    'data': [
        'views/product_variant_description_notes.xml',
        'reports/picking_report_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
    'price': 20,
    'currency': "EUR",
    'category': 'Sales'
}
