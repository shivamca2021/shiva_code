# -*- coding: utf-8 -*-
{
    'name': "web_icon_change_m_email",
    'sequence': 0,
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.ickpi.com",

    
    'category': 'Uncategorized',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mass_mailing',],
    'data': [
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': True,
}
