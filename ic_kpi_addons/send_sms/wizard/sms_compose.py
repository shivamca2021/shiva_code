# -*- coding: utf-8 -*-
import logging
from odoo import _, api, fields, models, SUPERUSER_ID


_logger = logging.getLogger(__name__)


class SMSComposer(models.TransientModel):
    _name = 'sms.compose'
    _description = 'SMS composition wizard'
    _log_access = True

    @api.onchange('template_id')
    def _get_body_text(self):
        self.body_text = self.template_id.sms_html
        self.gatewayurl_id = self.template_id.gateway_id

    template_id = fields.Many2one('send_sms', 'SMS Template')
    body_text = fields.Text('Body')
    gatewayurl_id = fields.Many2one('gateway_setup', 'SMS Gateway')

    def default_partner_ids(self):
        partner_ids = []
        active_model = self.env.context.get('active_model')

        if active_model == 'crm.lead':
            active_ids = self.env.context.get('active_ids')
            for rec in active_ids:
                record = self.env['crm.lead'].search([('id', '=', rec)])
                if record.partner_id:
                    partner_ids.append((4, record.partner_id.ids))
        if active_model == 'calendar.event':
            active_ids = self.env.context.get('active_ids')
            for rec in active_ids:
                record = self.env['calendar.event'].search([('id', '=', rec)])
                if record.partner_ids:
                    for partner in record.partner_ids:
                        partner_ids.append((4, partner.ids))
        return partner_ids

    partner_ids = fields.Many2many('res.partner', string='Contact', default=default_partner_ids)
    mobile = fields.Char(string='Mobile')

    def send_sms_action(self):
        active_model = self.env.context.get('active_model')
        model_id = self.env['ir.model'].search([('model', '=', active_model)])
        record_ids = self.env.context.get('active_ids')
        if active_model == 'calendar.event':
            if self.partner_ids:
                for rec in record_ids:
                    event = self.env['calendar.event'].search([('id', '=', rec)])

                    for partner in event.partner_ids:
                        if partner.phone or partner.mobile:
                            if partner.phone == partner.mobile:
                                mobile_no = partner.mobile
                                message = self.body_text
                                self.env['send_sms'].send_sms_link(rec, message, mobile_no, model_id.id, self.gatewayurl_id)

                            if partner.phone != partner.mobile:
                                if partner.phone:
                                    mobile_no = partner.phone
                                    message = self.body_text
                                    self.env['send_sms'].send_sms_link(rec, message, mobile_no, model_id.id,
                                                                             self.gatewayurl_id)
                                if partner.mobile:
                                    mobile_no = partner.mobile
                                    message = self.body_text
                                    self.env['send_sms'].send_sms_link(rec, message, mobile_no, model_id.id,
                                                                             self.gatewayurl_id)
        elif self.partner_ids:
            pos = 0
            for partner in self.partner_ids:
                if partner.phone or partner.mobile:
                    if partner.phone == partner.mobile:
                        mobile_no = partner.mobile
                        message = self.body_text
                        record = (record_ids[pos])
                        self.env['send_sms'].send_sms_link(record, message, mobile_no, model_id.id,
                                                               self.gatewayurl_id)

                    if partner.phone != partner.mobile:
                        if partner.phone:
                            mobile_no = partner.phone
                            message = self.body_text
                            record = (record_ids[pos])
                            self.env['send_sms'].send_sms_link(record, message, mobile_no, model_id.id,
                                                                   self.gatewayurl_id)
                        if partner.mobile:
                            mobile_no = partner.mobile
                            message = self.body_text
                            record = (record_ids[pos])
                            self.env['send_sms'].send_sms_link(record, message, mobile_no, model_id.id,self.gatewayurl_id)

                pos += 1

        else:
            record_id = self.env.context.get('active_id')
            mobile_no = self.mobile
            message = self.body_text
            self.env['send_sms'].send_sms_link(record_id, message, mobile_no, model_id.id, self.gatewayurl_id)
        return True
