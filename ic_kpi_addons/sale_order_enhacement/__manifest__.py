# -*- coding: utf-8 -*-

{
    'name': "SaleOrder Enhacement",
    'version': "14.0.1.2.2",
    'summary': """""",
    'description': """SaleOrder Enhacement""",
    'company': "IC-PRISM",
    'maintainer': "IC-PRISM",
    'website': "",
    'category': 'Tools',
    'depends': ['sale', 'base',],
    'data': [
        # 'data/data.xml',
        'security/ir.model.access.csv',
        'views/sale_order_inherit_view.xml',
        'views/sale_template_view.xml'
    ],
    'license': "AGPL-3",
    'installable': True,
    'application': True
}
