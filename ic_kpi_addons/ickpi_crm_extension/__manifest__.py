# -*- coding: utf-8 -*-

# Created on 2018-11-26
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# description:

{
    'name': 'CRM Extension App',
    'version': '14.0.0.1',
    'category': 'Productivity',
    "author": "IC-KPI",
    'license': 'LGPL-3',
    'sequence': 2,
    'summary': """
    Customize the crm module with some fields.
        """,
    'description': """

    Customize CRM module
    ============
    """,
    'images': ['static/description/banner.gif'],
    'depends': [
        'base',
        'crm',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'css': [],
    'js': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}
