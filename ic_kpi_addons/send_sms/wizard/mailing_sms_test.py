# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, _
import urllib
import requests
import re
import base64


class MassSMSTest(models.TransientModel):
    _inherit = 'mailing.sms.test'

    def send_sms_link(self):

        content = self.mailing_id.body_plaintext
        active_model = self.mailing_id.mailing_model_id
        sms_rendered_contents = content.encode('ascii', 'ignore')
        sms_rendered_content_msg = urllib.parse.quote_plus(sms_rendered_contents)
        rendered_sms_to = False
        if self.numbers:
            rendered_sms_to = re.sub(r' ', '', self.numbers)
            if '+' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('+', '')
            if '-' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('-', '')

        if rendered_sms_to:
            gateway = self.env['gateway_setup'].search([], limit=1)
            send_url = gateway.gateway_url
            send_link = send_url.replace('{mobile}', rendered_sms_to).replace('{message}', sms_rendered_content_msg).replace('{validity}', str(0))
            payload = {}
            string = gateway.key
            key = string.encode("ascii")
            base64_bytes = base64.b64encode(key)
            base64_message = base64_bytes.decode('ascii')
            headers = {
                'Authorization': 'Basic' + ' ' + base64_message
            }
            response = requests.request("GET", send_link, headers=headers, data=payload)
            if response.status_code and response.status_code == 200:
               resp = 'Success'
            else:
                resp = 'Failed'
            if active_model == 'res.partner':
                record_id = self.env.context.get('default_res_id')
            else:
                record_id = self.env.context.get('active_id')
                active_model = self.env.context.get('active_model')
            self.env['sms_track'].sms_track_create(record_id, content, rendered_sms_to, resp, active_model,
                                                   gateway.id)
            return response
