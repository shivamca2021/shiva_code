# -*- coding: utf-8 -*-
{
    'name' : 'Mass Email Management',
    'version' : '1.0',
    'summary': 'Application for the Email Management',
    'sequence': 10,
    'description': """Application for the Email Management and manage all emails""",
    'category': 'Sales',
    'depends' : ['contacts', 'mail', 'mass_mailing'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'views/res_partner.xml',
        'views/res_partner_groups_view.xml',
        'views/mailing_mailing_view.xml',
        'views/mail_template.xml',
        'wizard/template_name_wizard.xml',
    ],
    'demo': [
    ],
    'qweb': [
        'static/src/components/message/message.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
