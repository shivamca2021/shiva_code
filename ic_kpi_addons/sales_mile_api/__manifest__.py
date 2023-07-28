# -*- coding: utf-8 -*-

{
    'name': 'IC-KPI Mile APIs',
    'version': '14.0.0.1',
    "author": "IC-KPI",
    'category': 'Sales',
    'license': 'LGPL-3',
    'sequence': 2,
    'summary': """
    Sales APIs which provide flexibilities to the sales teams to link with mobile to increase the productivity.
        """,
    'description': """
    APP TO SALEs APIs
    =================
    - Sales meeting scheduling.
    - APIs to integrate with mobile.
    """,
    'images': ['static/description/banner.gif'],
    'depends': [
        'base_setup',
        'mail',
        'sales_mile',
        'hr',
    ],
    'data': [
        # 'views/employee_views.xml',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'css': [],
    'js': [],
    # 'pre_init_hook': 'pre_init_hook',
    # 'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': True,
}
