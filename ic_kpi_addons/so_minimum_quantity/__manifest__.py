{
    'name': "Sales Order Minimum Quantity",
    'author': '',
    'category': 'Sales',
    'summary': """Set minimum sales quantity limit on product""",
    'website': '',
    'description': """Sales Order Minimum Quantity""",
    'version': '14.0.1.0',
    'depends': ['base','sale_management','product','purchase'],
    'data': ['views/view_minimum_order_quantity.xml'
            ],
    'images': [''],
    'license': 'AGPL-3',    
    'installable': True,
    'application': True,
    'auto_install': False,
}
