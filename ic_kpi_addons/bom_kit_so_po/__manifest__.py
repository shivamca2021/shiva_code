# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Add BOM Kit product Based on Sale and Purchase ",
    "summary": "To Add Bom kit product base when product chooses in sale order and product order line ",
    "author": "",
    "website": "",
    "category": "Sale",
    "version": "14.0.1.0",

    "license": "AGPL-3",

    "depends": ["base", "sale_management", 'purchase'],
    'data': [
        'views/sale_order_custom.xml',
        'views/purchase_order_custom.xml',

    ],
    "demo": [],
    'installable': True,
    'auto_install': False,
    'application': True,

}
