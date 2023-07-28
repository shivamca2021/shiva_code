import logging
from odoo import api, fields, models, tools
_logger = logging.getLogger(__name__)


class sms_track(models.Model):
    _name = "sms_track"

    model_id = fields.Char('Model', readonly=True)
    record_id = fields.Integer(string="Record ID")
    mobile_no = fields.Char('Mobile No.', readonly=True)
    response_id = fields.Char('Response', readonly=True)
    message_id = fields.Text('Messages', readonly=True)
    gateway_id = fields.Many2one('gateway_setup', string='GateWay', readonly=True)
    view_record = fields.Boolean(string='View Record',compute='compute_view_record')

    @api.depends('model_id', 'record_id')
    def compute_view_record(self):
        for rec in self:
            if rec.model_id and rec.record_id:
                rec.view_record = True
            else:
                rec.view_record = False

    def show_record(self):
        if self.model_id and self.record_id:


            return {
                'name': '',
                'res_model': str(self.model_id),
                'res_id':  self.record_id,
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
            }

    @api.model
    def sms_track_create(self, record_id, sms_rendered_content, rendered_sms_to, response, model, gateway_id):
        if type(model) == int:
            model = self.env['ir.model'].search([('id', '=', model)], limit=1)
            value = {
                'model_id': model.model,
                'record_id': record_id,
                'mobile_no': rendered_sms_to,
                'message_id': sms_rendered_content,
                'response_id': response,
                'gateway_id': gateway_id,
            }
            track_id = self.create(value)
        else:
            value = {
                'model_id': model,
                'record_id': record_id,
                'mobile_no': rendered_sms_to,
                'message_id': sms_rendered_content,
                'response_id': response,
                'gateway_id': gateway_id,
            }
            track_id = self.create(value)

