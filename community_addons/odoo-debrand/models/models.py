# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class OdooDebrand(models.Model):
    """
     Fields to access from the database manager.
    """
    _inherit = "website"

    def get_company_logo(self):
        self.company_logo_url ="/web/image/res.company/%s/logo"%(self.id)

    def get_favicon(self):
        id = self.env['website'].sudo().search([])
        self.favicon_url ="/web/image/website/%s/favicon"%(id[0].id)

    favicon_url = fields.Text("Url", compute='get_favicon')
    company_logo_url = fields.Text("Url", compute='get_company_logo')
    
class Users(models.Model):
    """ Update of res.users class
        - add a preference about sending emails about notifications
        - make a new user follow itself
        - add a welcome message
        - add suggestion preference
        - if adding groups to a user, check mail.channels linked to this user
          group, and the user. This is done by overriding the write method.
    """
    _name = 'res.users'
    _inherit = ['res.users']
    _description = 'Users'

    notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in IC-KPI')],
        'Notification', required=True, default='email',
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email address\n"
             "- Handle in Odoo: notifications appear in your Odoo Inbox")
    
    odoobot_state = fields.Selection(
        [
            ('not_initialized', 'Not initialized'),
            ('onboarding_emoji', 'Onboarding emoji'),
            ('onboarding_attachement', 'Onboarding attachement'),
            ('onboarding_command', 'Onboarding command'),
            ('onboarding_ping', 'Onboarding ping'),
            ('idle', 'Idle'),
            ('disabled', 'Disabled'),
        ], string="IC-KPI Status", readonly=True, required=False) 
