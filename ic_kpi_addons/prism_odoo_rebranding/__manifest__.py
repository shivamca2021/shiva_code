
{
    'name': "Prism Odoo Debranding",

    'summary': """
        Odoo Module for backend and frontend debranding.""",

    'description': """
        To debrand front-end and back-end pages by removing
         odoo promotions, links, labels and other related
         stuffs.
    """,

    'author': "",
    'website': "",
    'category': 'Tools',
    'version': '14.0.5.0.3',
    'depends': [
        'base_setup',
        'web',
        'mail',
        'crm',
        'portal',
        'website',
        'mail_bot',
        'web_editor',
    ],
    'data': [
        'data/ir_config_parameter_data.xml',
        'data/ir_module_module_data.xml',
        'data/mail_template_data.xml',
        'data/res_company_data.xml',
        'data/mailbot_data.xml',
        'views/disable_odoo.xml',
        'views/views.xml',
    ],
    'qweb': ['static/src/xml/base.xml',
             'static/src/xml/notification_request.xml',
             'static/src/xml/media_placeholder.xml'],
    'images': ["static/description/banner.gif"],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
