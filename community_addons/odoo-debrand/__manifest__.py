# -*- coding: utf-8 -*-

{
    'name': "Debranding",
    'version': "14.0.1.2.2",
    'summary': """Debranding""",
    'description': """Debranding""",
    'live_test_url': '',
    'author': "shiva Singh",
    'company': "IC-PRISM",
    'maintainer': "IC-PRISM",
    'website': "",
    'category': 'Tools',
    'depends': ['website', 'base_setup'],
    'data': [
        'data/digest_tips_data.xml',
        'views/views.xml',
        'views/res_config_views.xml',
        'views/ir_module_views.xml'
    ],
    'qweb': ["static/src/xml/base.xml"],
    #'images': ['static/description/banner.gif'],
    'license': "AGPL-3",
    'installable': True,
    'pre_init_hook': '_pre_init_partner',
    'application': True
}
