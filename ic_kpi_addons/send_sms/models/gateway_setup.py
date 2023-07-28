from odoo import _, api, fields, models, tools
from odoo.exceptions import except_orm, UserError, Warning
import requests
import urllib
import re
import base64
import logging

_logger = logging.getLogger(__name__)


class GateWaysetup(models.Model):
    _name = "gateway_setup"
    _description = "GateWay Setup"

    name = fields.Char(required=True, string='Name')
    gateway_url = fields.Char(required=True, string='GateWay Url')
    body = fields.Text('Message')
    number = fields.Char('Mobile')
    username = fields.Char('Username')
    password = fields.Char('password')
    key = fields.Char(string='Key', compute='compute_key')
    response = fields.Char(string='Response')
    from_number = fields.Char('From')
    response_url = fields.Char(required=True, string='GateWay Response Url')

    def compute_key(self):
        for rec in self:
            if rec.username and rec.password:
               rec.key = rec.username + ':' + rec.password
            else:
                rec.key = False

    def send_sms_link(self, record_id, sms_rendered_content, rendered_sms_to,  model, gateway_url_id):
        sms_rendered_content = sms_rendered_content.encode('ascii', 'ignore')
        sms_rendered_content_msg = urllib.parse.quote_plus(sms_rendered_content)
        if rendered_sms_to:
            rendered_sms_to = re.sub(r' ', '', str(rendered_sms_to))
            if '+' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('+', '')
            if '-' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('-', '')

        if rendered_sms_to:
            send_url = gateway_url_id.gateway_url
            send_link = send_url.replace('{mobile}', rendered_sms_to).replace('{message}', sms_rendered_content_msg).replace('{validity}', str(0))
            payload = {}
            string = self.key
            key = string.encode("ascii")
            base64_bytes = base64.b64encode(key)
            base64_message = base64_bytes.decode('ascii')
            headers = {
                'Authorization': 'Basic' + ' ' + base64_message
            }
            try:
                response = requests.request("GET", send_link, headers=headers, data=payload)
                self.response = response
                response = requests.request("GET", url=send_link).text
                return response
            except Exception as e:
                return e

    # @api.one
    def sms_test_action(self):
        active_model = 'gateway_setup'
        message = self.env['send_sms'].render_template(self.body, active_model, self.id)
        mobile_no = self.env['send_sms'].render_template(self.number, active_model, self.id)
        response = self.send_sms_link(self.id, message, mobile_no, active_model, self)
        #response = self.send_sms_link(message, mobile_no, self.id, active_model, self)
        raise Warning(response)
