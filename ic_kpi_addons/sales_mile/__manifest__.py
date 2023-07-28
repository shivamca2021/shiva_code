{
    'name': 'Sales Mile',
    'category': 'CRM',
    "author": "IC-KPI",
    'summary': 'Sales Mile',
    'description': """
        Sales Mile
    """,
    'license': 'Other proprietary',
    'depends': ['base', 'crm', 'base_geolocalize', 'mail', 'utm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_trip_view.xml',
        'views/crm_view.xml',
        'views/trip_view.xml',
        'views/sequence.xml',
    ],

    'installable': True,
    'application': True,
}
