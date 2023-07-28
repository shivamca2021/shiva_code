
{
    'name': "Transfer Records to Different Instance",
    'summary': """
        Prism - Transfer Records to Different Instance.""",
    'description': """
        Prism - Transfer Records to Different Instance.
    """,
    'author': "FingertipIT",
    'website': "",
    'category': 'Tools',
    'version': '1.0',
    'depends': [
        'base_setup',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/transfer_record_view.xml',
    ],
    'qweb': [],
    'images': [],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}