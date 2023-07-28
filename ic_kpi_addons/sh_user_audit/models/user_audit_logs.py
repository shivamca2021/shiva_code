# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import logging
from odoo import http
from odoo.http import request, serialize_exception as _serialize_exception, content_disposition
from odoo import api, fields, models, tools, _
import datetime
from werkzeug import urls
import functools
import urllib
import requests
import re
import base64


class SmsSms(models.Model):
    _inherit = 'sms.sms'

    def sms_action_send(self,record_id, message, mobile_no, active_model, gateway):

        response = self.send_sms_link(record_id,message, mobile_no, active_model, gateway)

    def send_sms_link(self, record_id, sms_rendered_content, rendered_sms_to,  model, gateway_url_id):
        sms_rendered_contents = sms_rendered_content.encode('ascii', 'ignore')
        sms_rendered_content_msg = urllib.parse.quote_plus(sms_rendered_contents)
        if rendered_sms_to:
            rendered_sms_to = re.sub(r' ', '', rendered_sms_to)
            if '+' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('+', '')
            if '-' in rendered_sms_to:
                rendered_sms_to = rendered_sms_to.replace('-', '')

        if rendered_sms_to:
            gateway = self.env['gateway_setup'].search([], limit=1)
            send_url = gateway.gateway_url
            send_link = send_url.replace('{mobile}', rendered_sms_to).replace('{message}', sms_rendered_content_msg)
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
            self.env['sms_track'].sms_track_create(record_id, sms_rendered_content, rendered_sms_to, resp, model,
                                                   gateway.id)
            return response


class UserAudit(models.Model):
    _name = "sh.user.audit.log"
    _description = "User Audit Logs"

    object = fields.Many2one('ir.model', string="Object")
    record_id = fields.Integer(string="Record ID")
    name = fields.Char(string="Reference", readonly=True)
    user = fields.Many2one('res.users', string="User")
    type = fields.Selection([
        ("read", "Read"),
        ("write", "Write"),
        ("create", "Create"),
        ("delete", "Delete"),
    ], )
    modify_date = fields.Datetime(string="Date")
    updated_field = fields.Many2one('ir.model.fields', string="Update Field")
    value_updated = fields.Char("Updated Value")
    old_value = fields.Char("Old Values")
    log_id = fields.Many2one('log.custom' , string='Audit')

    @api.model
    def create(self, vals):

        vals.update(
            {"name": self.env["ir.sequence"].next_by_code("name.entry")})
        return super(UserAudit, self).create(vals)


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        records = super(BaseModel, self).create(vals_list)
        audit_log_id = self.env['sh.user.audit'].sudo().search([('is_create', '=', True),
                                                                ('model_ids.model', 'in', [
                                                                    self._name]),
                                                                '|', ('user_ids.id', 'in', [self.env.uid]),
                                                                ('is_all_users', '=', True)], limit=1)
        if audit_log_id:
            model_id = self.env['ir.model'].sudo().search(
                [('model', '=', self._name)], limit=1)
            for record in records:
                self.env['sh.user.audit.log'].sudo().create({'object': model_id.id,
                                                             'user': self.env.uid,
                                                             'type': 'create',
                                                             'record_id': record.id,
                                                             'modify_date': datetime.datetime.now()
                                                             })

        return records

    def unlink(self):
        if self._name not in (
        'ir.model.data', 'ir.config_parameter', 'ir.property', 'ir.default', 'ir.model.fields', 'ir.model.relation',
        'ir.module.module', 'ir.model'):
            audit_log_id = self.env['sh.user.audit'].sudo().search([('is_delete', '=', True),
                                                                    ('model_ids.model', 'in', [self._name]),
                                                                    '|', ('user_ids.id', 'in', [self.env.uid]),
                                                                    ('is_all_users', '=', True)], limit=1)
            if audit_log_id:
                model_id = self.env['ir.model'].sudo().search(
                    [('model', '=', self._name)], limit=1)
                for record in self.ids:
                    self.env['sh.user.audit.log'].sudo().create({'object': model_id.id,
                                                                 'user': self.env.uid,
                                                                 'type': 'delete',
                                                                 'record_id': record,
                                                                 'modify_date': datetime.datetime.now()
                                                                 })
        return super(BaseModel, self).unlink()

    def write(self, vals):

        if self._name not in (
        'ir.model.data', 'ir.config_parameter', 'ir.property', 'ir.default', 'ir.model.fields', 'ir.model.relation',
        'ir.module.module', 'ir.model', 'log.custom',):
            audit_log_id = self.env['sh.user.audit'].sudo().search([('is_write', '=', True),
                                                                    '|', ('user_ids.id', 'in', [self.env.uid]),
                                                                    ('is_all_users', '=', True)], limit=1)
            current_rec = False
            field_log_track = False
            field_lists = []
            if audit_log_id:
                for rec in self:
                    model_id = self.env['ir.model'].sudo().search(
                        [('model', '=', self._name)], limit=1)
                    audit = self.env['log.custom'].search([('model_id', '=', model_id.id)])

                    audit_id = False
                    for aud in audit:

                        audit_id = aud

                    if model_id and audit_id:
                        list_of_ids = False
                        for key in vals:
                            field_lists.append(key)
                            field_log_track = audit_log_id.field_ids.filtered(
                                lambda x: x.model_id.id == model_id.id and x.name == key)
                            updated_field = self.env['ir.model.fields'].search([('name', '=', key), ('model_id', '=', model_id.id)], limit=1)
                            if updated_field.ttype == 'many2many':
                                related_model = updated_field.relation

                                if vals[key]:
                                    if type(vals[key][0]) == tuple:
                                        list_of_ids = vals[key][0]
                                    else:
                                        list_of_ids = vals[key][0][2]
                                updated_list = []
                                old_list = []
                                for upd_id in list_of_ids:
                                   updated_val = self.env[related_model].search([('id', '=', upd_id)], limit=1)
                                   updated_list.append(updated_val.name)
                                if field_log_track:

                                    if audit_log_id.is_full_log:

                                        current_rec = self.env[model_id.model].search_read([('id', '=', rec.id)], [key])

                                        if current_rec:
                                            if current_rec[0]:
                                                for old_id in current_rec[0].get(key):
                                                    old_val = self.env[related_model].search([('id', '=', old_id)], limit=1)
                                                    old_list.append(old_val.name)

                                            self.env['sh.user.audit.log'].sudo().create({'object': model_id.id,
                                                                                         'user': self.env.uid,
                                                                                         'type': 'write',
                                                                                         'record_id': rec.id,
                                                                                         'modify_date': datetime.datetime.now(),
                                                                                         'log_id': audit_id.id,
                                                                                         'updated_field': field_log_track.id,
                                                                                         'value_updated': updated_list,
                                                                                         'old_value': old_list
                                                                                         })
                                    else:

                                        self.env['sh.user.audit.log'].sudo().create({'object': model_id.id,
                                                                                     'user': self.env.uid,
                                                                                     'type': 'write',
                                                                                     'record_id': self.id,
                                                                                     'modify_date': datetime.datetime.now()})

                            elif updated_field.ttype == 'many2one':
                                related_model = updated_field.relation
                                updated_val = self.env[related_model].search([('id', '=', vals[key])], limit=1)

                                if field_log_track:
                                    if audit_log_id.is_full_log:
                                        current_rec = self.env[model_id.model].search_read( [('id', '=', rec.id)], [key])

                                        if current_rec:
                                            self.env['sh.user.audit.log'].sudo().create({'object': model_id.id,
                                                                                         'user': self.env.uid,
                                                                                         'type': 'write',
                                                                                         'record_id': rec.id,
                                                                                         'modify_date': datetime.datetime.now(),
                                                                                         'log_id': audit_id.id,
                                                                                         'updated_field': field_log_track.id,
                                                                                         'value_updated': updated_val.name,
                                                                                         'old_value': current_rec[0].get(
                                                                                             key)
                                                                                         })
                                    else:
                                        self.env['sh.user.audit.log'].sudo().create({'object': model_id.id,
                                                                                     'user': self.env.uid,
                                                                                     'type': 'write',
                                                                                     'record_id': self.id,
                                                                                     'modify_date': datetime.datetime.now(), })
                            else:

                                if field_log_track:
                                    if audit_log_id.is_full_log:
                                        current_rec = self.env[model_id.model].search_read(
                                            [('id', '=', rec.id)], [key])
                                        if current_rec:
                                            self.env['sh.user.audit.log'].sudo().create({'object': model_id.id,
                                                                                         'user': self.env.uid,
                                                                                         'type': 'write',
                                                                                         'record_id': rec.id,
                                                                                         'modify_date': datetime.datetime.now(),
                                                                                         'log_id': audit_id.id,
                                                                                         'updated_field': field_log_track.id,
                                                                                         'value_updated': vals[key],
                                                                                         'old_value': current_rec[0].get(
                                                                                             key)
                                                                                         })
                                    else:
                                        self.env['sh.user.audit.log'].sudo().create({'object': model_id.id,
                                                                                     'user': self.env.uid,
                                                                                     'type': 'write',
                                                                                     'record_id': self.id,
                                                                                     'modify_date': datetime.datetime.now(),})

                    table = ''
                    tr = ''
                    th = ''
                    td = ''
                    tr1 = ''
                    table += '''
                    <table class="table table-bordered" width="100%" style="padding:0px;">'''
                    tr += '''<tr>'''
                    th += '''<tr>
                                 <th class="th_custom">''' + 'Updated Field' + '''<br></th>
                                 <th class="th_custom">''' + 'Old Value' + '''<br></th>
                                 <th class="th_custom">''' + 'Updated Value' + '''<br></th></tr>
                                                          '''
                    tr += '''</tr>'''
                    table += th
                    updated_value = False

                    if field_lists:

                        for field in field_lists:

                            current_rec = self.env[model_id.model].search_read(
                                [('id', '=', rec.id)], [field])

                            updated_field = self.env['ir.model.fields'].search(
                                [('name', '=', field), ('model_id', '=', model_id.id)], limit=1)
                            related_model = updated_field.relation

                            if updated_field.ttype == 'many2many':
                                if type(vals[field][0]) == tuple:
                                    list_of_ids = vals[field][0]
                                else:
                                    list_of_ids = vals[field][0][2]
                                updated_list = []
                                old_list = []
                                for upd_id in list_of_ids:
                                    updated_val = self.env[related_model].search([('id', '=', upd_id)], limit=1)
                                    updated_list.append(updated_val.name)

                                for old_id in current_rec[0].get(field):
                                    old_value = self.env[related_model].search([('id', '=', old_id)], limit=1)
                                    old_list.append(old_value.name)

                            if updated_field.ttype == 'many2one':
                                updated_value = self.env[related_model].search([('id', '=', vals[field])], limit=1)
                            field_log_track = audit_log_id.field_ids.filtered(
                                lambda x: x.model_id.id == model_id.id and x.name == field)

                            if field_log_track:
                                if str(current_rec[0].get(field)) == 'False':

                                    old_val = ''
                                else:
                                    old_val = str(current_rec[0].get(field))

                                tr1 += '''<tr>'''
                                td = '''<tr>
                                     <td style="text-align:center" rowspan="1">''' + str(field_log_track.field_description) + '''<br></td>'''
                                if updated_field.ttype == 'many2many':
                                    td += '''<td style="text-align:center" rowspan="1">''' +str(old_list) + '''<br></td>'''
                                else:
                                    td += '''<td style="text-align:center" rowspan="1">''' + old_val + '''<br></td>'''
                                if updated_field.ttype == 'many2many':
                                    td += '''<td style="text-align:center" rowspan="1">''' + str(updated_list) + '''<br></td></tr> '''
                                elif updated_field.ttype == 'many2one':
                                    td += '''<td style="text-align:center" rowspan="1">''' + str(updated_value.name) + '''<br></td></tr> '''

                                else:
                                    td += '''<td style="text-align:center" rowspan="1">''' + str(
                                        vals[field]) + '''<br></td></tr> '''
                                tr1 += '''</tr>'''
                                table += td

                        table += '''</table>'''
                        conf_objs = self.env['sh.user.audit'].sudo().search([], limit=1)
                        conf = False
                        if conf_objs:
                            for obj in conf_objs:

                                if obj.model_ids:
                                    if obj.model_ids[0] == model_id:
                                        conf = obj
                        field_track = audit_log_id.mapped('field_ids.name')
                        common_fields = set(field_lists) & set(field_track)
                        if common_fields:
                            for record in conf_objs.user_line_ids:
                                if record.notification_type == 'mail':
                                    mail_content = record.mail_template.replace('${table}', table).replace('${module}',model_id.name).replace('${ref}',rec.name).replace('${user}', self.env.user.name)
                                    ctx = {
                                            'default_model': 'sh.user.audit',
                                            # 'default_res_id': record,
                                            'default_body': mail_content,
                                            # 'proforma': self.env.context.get('proforma', False),
                                        }
                                    values = {
                                            'subject': 'Changes made',
                                            'recipient_ids': record.partner_ids.ids,
                                            'body_html': mail_content,
                                        }
                                    mail_id = self.env['mail.mail'].with_context(ctx).create(values)
                                    mail_id.send()
                                if record.notification_type == 'sms':
                                    sms_content = record.sms_template.replace('${module}', model_id.name)
                                    for partner in record.partner_ids:
                                        if partner.phone or partner.mobile:
                                            if partner.phone == partner.mobile:
                                                values = {
                                                    'body': sms_content,
                                                    'number': partner.mobile,
                                                }
                                                sms = self.env['sms.sms'].create(values)
                                                gateway = self.env['gateway_setup'].search([], limit=1)
                                                sms.sms_action_send(rec.id, sms_content, partner.mobile,  model_id.id, gateway.id)
                                            if partner.phone != partner.mobile:
                                                if partner.phone:
                                                    values = {
                                                        'body': sms_content,
                                                        'number': partner.phone,
                                                    }
                                                    sms = self.env['sms.sms'].create(values)
                                                    gateway = self.env['gateway_setup'].search([], limit=1)
                                                    sms.sms_action_send(rec.id,sms_content, partner.phone, model_id.id, gateway.id)
                                                if partner.mobile:
                                                    values = {
                                                        'body': sms_content,
                                                        'number': partner.mobile,
                                                    }
                                                    sms = self.env['sms.sms'].create(values)
                                                    gateway = self.env['gateway_setup'].search([], limit=1)
                                                    sms.sms_action_send(rec.id,sms_content, partner.mobile, model_id.id, gateway.id)

        return super(BaseModel, self).write(vals)
