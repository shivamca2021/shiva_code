# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json
import base64
import requests
from datetime import datetime


class MailingTrace(models.Model):

    _inherit = 'mailing.trace'

    @api.depends('model','res_id')
    def _get_partner(self):
        for mass_trace in self:
            if mass_trace.model == 'res.partner':
                partner = self.env['res.partner'].search([('id','=',mass_trace.res_id)])
                if partner:
                    mail_contact = self.env[mass_trace.model].browse(mass_trace.res_id)
                    if mail_contact._name == 'res.partner':
                        mass_trace.partner_id = mail_contact.id

    sms_message_id = fields.Char(string='Message-ID')
    get_response = fields.Boolean(default=False)
    replied_message = fields.Char(string='Message')
    partner_id = fields.Many2one('res.partner',compute='_get_partner', store=True )
    original_message = fields.Char(string='Message')
    
    @api.model
    def _get_sms_response(self):
        mass_traces = self.search([('get_response','=',False),('sms_message_id','!=',False),('trace_type','=','sms')])
        gateway = self.env['gateway_setup'].search([], limit=1)
        send_url = gateway.response_url
        for mass_trace in mass_traces:
            send_link = send_url.replace('{message_id}', mass_trace.sms_message_id)
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
                response_dict = json.loads(response.text)
                subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment')
                if 'responses' in response_dict:
                    for res in response_dict['responses']:
                        mail_contact = self.env[mass_trace.model].browse(mass_trace.res_id)
                        if mail_contact._name == 'res.partner':
                            mail_contact.message_post(
                                    partner_ids=mail_contact.ids,
                                    body=res['response'],
                                    message_type='comment', subtype_id=subtype_id
                                )
                        else:
                            mail_contact.message_post(
                                    body=res['response'],
                                    message_type='comment', subtype_id=subtype_id
                                )
                        mass_trace.replied_message = res['response']
                    mass_trace.state = 'replied'
                    mass_trace.get_response = True
                    mass_trace.replied = datetime.now()

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            if 'skip' in self._context:
                break
            if 'sms_sms_id' in values:
                values['sms_sms_id_int'] = values['sms_sms_id']
            if values.get('trace_type') == 'sms' and not values.get('sms_code'):
                values['sms_code'] = self._get_random_code()
            gateway = self.env['gateway_setup'].search([], limit=1)
            number = False
            record_id = False
            model = False
            mass_mailing_id = False
            list_rec = []
            if values.get('sms_number', False):
                number = values.get('sms_number', False)
            if values['res_id']:
                record_id = values['res_id']
                list_rec.append(record_id)
            if values['model']:
                model = values['model']
            if values['mass_mailing_id']:
                mass_mailing_id = values['mass_mailing_id']
            mass_mail = self.env['mailing.mailing'].search([('id', '=', mass_mailing_id)], limit=1)
            body = mass_mail.body_plaintext
            all_bodies = self.env['mail.render.mixin']._render_template(body, model, list_rec)

            message = list(all_bodies.items())[0]
            send_url = gateway.gateway_url
            if message and number:
                send_link = send_url.replace('{mobile}', number).replace('{message}', message[1]).replace('{validity}', str(0)).replace('{from}', gateway.from_number)
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
                    response_dict = json.loads(response.text)
                    message_id = response_dict.get('message_id')
                    url = 'https://api.transmitsms.com/get-sms.json/?message_id=%s&validity=%s' % (message_id, 0)
                    msg_response = requests.request("POST", url, headers=headers, data=payload)

                    msg_response_dict = json.loads(msg_response.text)
                    delivery_stats = msg_response_dict.get('error')
                    if delivery_stats['code'] == 'SUCCESS':
                        values['sent'] = datetime.now()
                        values['sms_message_id'] = str(message_id)
                        values['original_message'] = body
                    elif delivery_stats['bounced'] == 1:
                        values['bounced'] = datetime.now()

                else:
                    resp = 'Failed'
                    values['exception'] = datetime.now()
                track = self.env['sms_track'].sms_track_create(record_id, message[1], number, resp, model,
                                                       gateway.id)
            else:
                values['exception'] = datetime.now()
        return super(MailingTrace, self).create(values_list)

    def set_failed(self, failure_type):
        for trace in self:
            if trace._context.get('default_mailing_type'):
                if trace._context.get('default_mailing_type') == 'sms':
                    pass
                else:
                    trace.write({'exception': fields.Datetime.now(), 'failure_type': failure_type})

    def set_sms_sent(self, sms_sms_ids=None):
        if self._context.get('default_mailing_type'):
            if self._context.get('default_mailing_type') == 'sms':
                pass
            else:
                statistics = self._get_records_from_sms(sms_sms_ids, [('sent', '=', False)])
                statistics.write({'sent': fields.Datetime.now()})
                return statistics

    def set_sms_clicked(self, sms_sms_ids=None):
        if self._context.get('default_mailing_type'):
            if self._context.get('default_mailing_type') == 'sms':
                pass
            else:
                statistics = self._get_records_from_sms(sms_sms_ids, [('clicked', '=', False)])
                statistics.write({'clicked': fields.Datetime.now()})
                return statistics

    def set_sms_ignored(self, sms_sms_ids=None):
        if self._context.get('default_mailing_type'):
            if self._context.get('default_mailing_type') == 'sms':
                pass
            else:
                statistics = self._get_records_from_sms(sms_sms_ids, [('ignored', '=', False)])
                statistics.write({'ignored': fields.Datetime.now()})
                return statistics

    def set_sms_exception(self, sms_sms_ids=None):
        if self._context.get('default_mailing_type'):
            if self._context.get('default_mailing_type') == 'sms':
                pass
            else:
                statistics = self._get_records_from_sms(sms_sms_ids, [('exception', '=', False)])
                statistics.write({'exception': fields.Datetime.now()})
                return statistics

class mailingmailing(models.Model):
    _inherit = "mailing.mailing"
    
    @api.constrains('sms_allow_unsubscribe')
    def _onchange_opt_out(self):
        if self.sms_allow_unsubscribe:
            self.body_plaintext = self.body_plaintext + ' [unsub-reply-link] '

    def action_view_sms_traces_replied(self):
        return self._action_view_sms_traces_filtered('replied')
    
    def _action_view_sms_traces_filtered(self, view_filter):
        if view_filter == 'replied':
            opened_stats = self.mailing_trace_ids.filtered(lambda stat: stat[view_filter])
        else:
            opened_stats = self.env['mailing.trace']
        res_ids = opened_stats.ids
        model_name = self.env['ir.model']._get(self.mailing_model_real).display_name
        return {
            'name': model_name,
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'mailing.trace',
            'views': [(self.env.ref('send_sms.mailing_trace_view_tree_sms_inherit').id, 'tree'),(self.env.ref('send_sms.mailing_trace_view_form_sms_inheirt').id, 'form')],
            'domain': [('id', 'in', res_ids)],
            'context': dict(self._context, create=False)
        }
