{
    'name': 'Insurance Management',
    'category': 'Insurance',
    'summary': 'Insurance Management.',
    'version': '1.0',
    'description': """Insurance Management""",
    'depends': [
        'contacts','sale','account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/insurance.xml',
    ],
    'installable': True,
    'auto_install': False,
}
