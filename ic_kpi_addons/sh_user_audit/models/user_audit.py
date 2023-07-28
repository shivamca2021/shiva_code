# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UserAudit(models.Model):
    _name = "sh.user.audit"
    _description = "User Audit"

    name = fields.Char(string="Name", required=True)
    conf_name = fields.Char(string="Configuration Name")
    is_full_log = fields.Boolean(string="Full Log")
    is_read = fields.Boolean(string="Read")
    is_write = fields.Boolean(string="Write")
    is_create = fields.Boolean(string="Create")
    is_delete = fields.Boolean(string="Delete")
    is_all_users = fields.Boolean(string="All Users")
    user_ids = fields.Many2many('res.users',
                                string="Users",
                                domain="[('share','=',False)]")
    model_ids = fields.Many2many("ir.model")
    field_ids = fields.Many2many("ir.model.fields")
    user_line_ids = fields.One2many('audit.user.line', 'audit_id', string='User Line')

    def _get_default_note(self):
        result = """
           <div>
               <p >These fields are changed by ${user} in ${module}</p>
               <br/>
               <p>${table}</p>
           </div>"""

        return result

    def _get_default_sms(self):
        result = """ALERT fields are changed in ${module}"""

        return result

    mail_template = fields.Html(string='Mail', default=_get_default_note)
    notification_User_ids = fields.Many2many('res.users','audit_log','model', string='Notification User')
    sms_template = fields.Text("Alert content", default=_get_default_sms)
    notification_type = fields.Selection([('mail', 'Mail'), ('sms', 'SMS')], default="mail", string='Notification Type')
    selected_model_ids = []

    @api.onchange("model_ids")
    def _onchange_model_ids(self):
        for i in self.model_ids:
            self.selected_model_ids.append(i.name)


class AuditLine(models.Model):
    _name = 'audit.user.line'

    sms_template = fields.Text(string='Sms Template')
    mail_template = fields.Html(string='Mail Template')
    notification_type = fields.Selection([('mail', 'Mail'), ('sms', 'SMS')],  string='Notification Type')
    partner_ids = fields.Many2many('res.partner', string='Users')
    audit_id = fields.Many2one('sh.user.audit', string='Audit Id')
