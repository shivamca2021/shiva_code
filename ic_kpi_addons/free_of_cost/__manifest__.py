# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Free of Cost in Sale order  ",
    "summary": "Free of Cost in  Sale and ",
    "author": "",
    "website": "",
    "category": "Sale",
    "version": "14.0.1.0",

    "license": "AGPL-3",

    "depends": ["base", "sale_management", ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_custom_views.xml',
        'views/free_of_cost_views.xml'
    ],
    "demo": [],
    'installable': True,
    'auto_install': False,
    'application': True,

}
