from odoo import api, fields, models
from urllib.parse import urlparse, urlunparse, parse_qs
import base64


class LogModels(models.Model):
    _name = "log.custom"

    name = fields.Char('Name')

    notification_type = fields.Selection([('mail', 'Mail'), ('sms', 'Sms')], default="mail", string='Notification Type')
    User_ids = fields.Many2many('res.users', string='Notification User', default=lambda self: self.env.user)
    sms_text = fields.Text("Alert content")
    mail_temp = fields.Html(string='Alert content')

    def _get_default_image(self):
        url = self.env.context.get('alert_url')
        uri = urlparse(url)
        qs = uri.fragment
        if parse_qs(qs).get('menu_id', None):
            menu_id = parse_qs(qs).get('menu_id', None)[0]
            menu = self.env['ir.ui.menu'].search([('id', '=', menu_id)])
            icon = menu.web_icon_data
            return icon

    def _default_audit_id(self):
        return self.env['sh.user.audit'].search([], limit=1).id

    audit_id = fields.Many2one('sh.user.audit', "Audit Log ", default=_default_audit_id)
    log_line_ids = fields.One2many('log.line', 'log_id', string='Log Line')

    def _default_model(self):
        url = self.env.context.get('alert_url')
        uri = urlparse(url)
        qs = uri.fragment
        if parse_qs(qs).get('model', None):
            model = parse_qs(qs).get('model', None)[0]
            model_ids = []
            active_model = self.env['ir.model'].sudo().search([('model', '=', model)], limit=1)
            model_ids.append((4, active_model.id))
            return active_model.id

    model_ids = fields.Many2many('ir.model', string='Model' )
    model_id = fields.Many2one('ir.model', string='Model', default=_default_model)
    field_ids = fields.Many2many('ir.model.fields', string='Fields ', domain="[('model_id.id','in',model_ids)]")

    module_icon = fields.Binary(string="Module Icon", default=_get_default_image)
    heading = fields.Char(string="Heading")

    @api.onchange('model_id')
    def _onchange_model_id(self):

        model_ids=[]
        model_ids.append(self.model_id.id)
        self.model_ids = [(6, 0, model_ids)]
        if self.model_id:
            self.heading = 'Customize Your Alert Notification for' + ' ' + self.model_id.name
            log = self.env['log.custom'].search([('model_id', '=', self.model_id.id)], limit=1)
            if log:
               self.name = log.name
            else:
                self.name = False

    @api.onchange('audit_id')
    def _onchange_audit_id(self):

        for rec in self:
            rec.field_ids = False
            rec.model_ids = False
            rec.log_line_ids = False
            if rec.audit_id:
                rec.name = rec.audit_id.conf_name if rec.audit_id.conf_name else False
                rec.field_ids = rec.audit_id.field_ids if rec.audit_id.field_ids  else False
                rec.model_ids = rec.audit_id.model_ids.ids if rec.audit_id.model_ids  else False
                user_list = []
                for line in rec.audit_id.user_line_ids:
                    vals = {'partner_ids': line.partner_ids.ids,
                            'notification_type': line.notification_type,
                            'mail_template': line.mail_template if line.mail_template else False,
                            'sms_template': line.sms_template if line.sms_template else False,
                            }
                    user_list.append((0, 0, vals))
                rec.log_line_ids = user_list

    def set_alert(self):
        user_list=[(5, 0, 0)]
        for rec in self:
            if rec.audit_id:
                rec.audit_id.conf_name = rec.name
                rec.audit_id.model_ids = rec.model_ids
                rec.audit_id.field_ids = rec.field_ids

            for line in rec.log_line_ids:
                vals = {'partner_ids': line.partner_ids.ids,
                        'notification_type': line.notification_type,
                        'mail_template': line.mail_template if line.mail_template else False,
                        'sms_template': line.sms_template if line.sms_template else False,
                        }
                user_list.append((0, 0, vals))
            rec.audit_id.user_line_ids = user_list
            log = self.search([('model_id', '=', self.model_id.id)])
            if log:
                for rec in log:
                    rec.write({'name': self.name})


class LogLine(models.Model):
    _name = "log.line"

    sms_template = fields.Text(string='Sms Template')
    mail_template = fields.Html(string='Mail Template')
    body_html = fields.Html(string='Mail new temp')
    notification_type = fields.Selection([('mail', 'Mail'), ('sms', 'SMS')],  string='Notification Type')
    partner_ids = fields.Many2many('res.partner', string='User')
    log_id = fields.Many2one('log.custom', string='Log Id')

    @api.onchange('notification_type')
    def onchange_notification_type(self):
        if self.notification_type == 'sms':
            self.sms_template = self.log_id.audit_id.sms_template
        if self.notification_type == 'mail':
            self.mail_template = self.log_id.audit_id.mail_template

