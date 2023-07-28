# -*- coding: utf-8 -*-

from odoo import fields, models
import urllib
import requests
import re
import base64
import json


class SMSComposer(models.TransientModel):
    _inherit = 'sms.composer'

    def send_sms_link(self):

        content = self.body
        active_model = self.env.context.get('default_res_model')
        sms_rendered_contents = content.encode('ascii', 'ignore')
        sms_rendered_content_msg = urllib.parse.quote_plus(sms_rendered_contents)
        rendered_sms_to = False
        if self.recipient_single_number_itf:
            rendered_sms_to = re.sub(r' ', '', self.recipient_single_number_itf)
            if '+' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('+', '')
            if '-' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('-', '')

        if rendered_sms_to:
            gateway = self.env['gateway_setup'].search([], limit=1)
            send_url = gateway.gateway_url
            send_link = send_url.replace('{mobile}', rendered_sms_to).replace('{message}', sms_rendered_content_msg).replace('{validity}', str(0)).replace('{from}', gateway.from_number)
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
                response_dict = json.loads(response.text)
                message_id = response_dict.get('message_id')
                trace_code = self.env['mailing.trace']._get_random_code()
                trace_values = {
                        'model': 'res.partner',
                        'res_id': record_id,
                        'trace_type': 'sms',
                        'sms_number': rendered_sms_to,
                        'sms_code': trace_code,
                        'sms_message_id':str(message_id),
                        'get_response':False,
                        'mass_mailing_id':False,
                        'original_message':content
                        
                    }
                self.env['mailing.trace'].with_context({'skip':True}).create(trace_values)
                mail_contact = self.env['res.partner'].browse(record_id)
                subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment')
                mail_contact.message_post(
                        partner_ids=mail_contact.ids,
                        body=self.body,
                        message_type='comment', subtype_id=subtype_id
                    )
            else:
                record_id = self.env.context.get('active_id')
                active_model = self.env.context.get('active_model')
            self.env['sms_track'].sms_track_create(record_id, self.body, rendered_sms_to, resp, active_model,
                                                   gateway.id)
            return response

    def _prepare_mass_sms_trace_values(self, record, sms_values):
        trace_code = self.env['mailing.trace']._get_random_code()
        trace_values = {
            'model': self.res_model,
            'res_id': record.id,
            'trace_type': 'sms',
            'mass_mailing_id': self.mailing_id.id,
            'sms_number': sms_values.get('number', False),
            'sms_code': trace_code,
        }
        return trace_values
