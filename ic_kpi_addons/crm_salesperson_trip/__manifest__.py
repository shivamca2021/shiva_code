# -*- coding: utf-8 -*-
{
    'name': 'CRM Salesperson Trip',
    'category': 'Extra Tools',
    'version': '14.0.1.0.5',
    'summary': 'Assigned your salesperson to visit potential customer',
    'description': """
""",
    'author': 'Yopi Angi',
    'depends': [
        'web_google_maps',
        'crm_maps',
        'contacts_maps',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/crm_salesperson_trip_line.xml',
        'views/crm_salesperson_trip.xml',
        'wizard/crm_salesperson_trip_line_note.xml',
    ],
    'demo': [],
    'qweb': ['static/src/xml/sidebar_direction.xml'],
    'pre_init_hook': 'pre_init_hook',
}
