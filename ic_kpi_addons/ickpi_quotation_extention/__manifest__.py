{
    'name': 'Quotation Changes',
    "author": "IC-KPI",
    'category': 'Sale',
    'summary': 'Quotation Changes',
    'description': """
        Quotation Changes
    """,
    'license': 'Other proprietary',
    'depends': ['base', 'sale', 'sale_management'],
    'data': [
        'views/sale_view.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'application': True,
}
