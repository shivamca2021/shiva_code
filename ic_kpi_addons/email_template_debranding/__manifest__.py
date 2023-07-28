
{
    'name': "Email Template Debranding",

    'summary': """
        Odoo Module Email Template debranding.""",

    'description': """
        Odoo Module Email Template debranding.
    """,

    'author': "",
    'website': "",
    'category': 'Tools',
    'version': '14.0.5.0.3',
    'depends': [
        'mail',
        'gamification',
        'crm_iap_lead',
        'website_crm_partner_assign',
        'calendar',
    ],
    'data': [
        'data/mail_template_data.xml',
        'data/mail_template.xml',
    ],
    'qweb': ['static/src/xml/base.xml'],
    'images': ["static/description/banner.gif"],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
