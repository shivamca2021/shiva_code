# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Rename Qweb report in Sale order and Purchase order ",
    "summary": "Rename the Qweb report  Sale and Purchase Order",
    "author": "",
    "website": "",
    "category": "Sale",
    "version": "14.0.1.0",

    "license": "AGPL-3",

    "depends": ["base", "sale_management", 'purchase'],
    'data': [
        'views/sale_report_custom_views.xml',
    ],
    "demo": [],
    'installable': True,
    'auto_install': False,
    'application': True,

}
