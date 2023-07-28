# -*- coding: utf-8 -*-
from odoo import fields, models


class CrmSalespersonTripLineNote(models.TransientModel):
    _name = 'crm.salesperson.trip.line.note'
    _description = 'Salesperson Trip line note'

    note = fields.Text(
        string='Note',
        required=True,
    )
    trip_line_id = fields.Many2one(
        comodel_name='crm.salesperson.trip.line',
        string='Trip',
        required=True,
    )
    trip_datetime = fields.Datetime(
        default=lambda self: fields.Datetime.now(),
        string='Visit Date',
    )

    def action_set_note(self):
        self.trip_line_id.write(
            {
                'notes': self.note,
                'is_visited': True,
                'trip_datetime': self.trip_datetime,
            }
        )
        self.trip_line_id.trip_id.message_post(
            body='Visit note of {} on {}: {}'.format(
                self.trip_line_id.lead_id.display_name,
                self.trip_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                self.note,
            ),
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )
        return {'type': 'ir.actions.act_window_close'}
