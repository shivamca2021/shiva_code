# -*- coding: utf-8 -*-
{
    'name': "web_icon_change",
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
                'mail',
                'sale',
                'website',
                'point_of_sale',
                'stock',
                'purchase',
                'hr',
                'hr_attendance',
                'contacts',
                'hr_holidays',
                'fleet',
                'project',
                'hr_expense',
                'survey',
                'crm',
                'event',
                'website_slides',
                'mrp',
                'maintenance',
                'note',
                'mass_mailing',
                'mass_mailing_sms',
                'lunch',
                'hr_recruitment',
                'account',
                'im_livechat',
                'ks_dashboard_ninja',
                'sign'],
    'data': [
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': True,
}
