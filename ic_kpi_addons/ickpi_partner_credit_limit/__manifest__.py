{
    'name': 'Partner Credit Limit',
    "author": "IC-KPI",
    'category': 'Partner',
    'summary': 'Partner Credit Limit',
    'description': """
        Partner Credit Limit
    """,
    'license': 'Other proprietary',
    'depends': ['base', 'contacts', 'account', 'ickpi_quotation_extention',
                'account_followup'],
    'data': [
        'views/partner_view.xml',
    ],

    'installable': True,
    'application': True,
}
