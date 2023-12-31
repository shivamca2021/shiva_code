{
    'name': "Send SMS",
    'version': '0.1',
    'author': "Debasish Dash",
    'category': 'Tools',
    'summary': 'You can use multiple gateway for multiple sms template to send SMS.',
    'description': 'Allows you to send SMS to the mobile no.',
    'website': "http://www.debweb.com",
    'depends': ['base', 'web', 'sms', 'mail', 'mass_mailing_sms','crm_sms'],
    'data': [
        'view/send_sms_view.xml',
        'view/ir_actions_server_views.xml',
        'view/sms_track_view.xml',
        'view/gateway_setup_view.xml',
        'view/mailing.xml',
        'view/res_partner.xml',
        'wizard/sms_compose_view.xml',
        'wizard/sms_composer.xml',
        'wizard/mailing_sms_test.xml',
        'security/ir.model.access.csv',
        'data/cron.xml'
    ],
    'images':['static/description/banner.png'],
    # 'license': 'LGPL-3',
    'installable':True,
    'auto_install':False,
}
