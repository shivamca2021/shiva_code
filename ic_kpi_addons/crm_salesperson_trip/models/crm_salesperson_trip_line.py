# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models


class CrmSalespersonTripLine(models.Model):
    _name = 'crm.salesperson.trip.line'
    _description = 'CRM Salesperson Trip Line'
    _rec_name = 'lead_id'
    _order = 'sequence, distance'

    @api.depends('lead_id', 'partner_id')
    def _compute_geolocalize(self):
        for trip in self:
            if trip.lead_id:
                trip.latitude = trip.lead_id.customer_latitude
                trip.longitude = trip.lead_id.customer_longitude
            elif trip.partner_id:
                trip.latitude = trip.partner_id.partner_latitude
                trip.longitude = trip.partner_id.partner_longitude
            else:
                trip.latitude = 0.0
                trip.longitude = 0.0

    @api.depends('lead_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.lead_id:
                rec.name = rec.lead_id.display_name
            elif rec.partner_id:
                rec.name = rec.partner_id.display_name
            else:
                rec.name = 'Unknown'

    name = fields.Char(string='Name', compute='_compute_name')
    trip_id = fields.Many2one(
        comodel_name='crm.salesperson.trip',
        string='Trip',
        required=True,
        ondelete='cascade',
    )
    source_data = fields.Selection(
        selection=[
            ('lead', _('Lead/Opportunity')),
            ('contact', _('Contacts')),
        ],
        default='lead',
        string='Data source',
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead/Opportunity',
        ondelete='cascade',
        domain=[
            ('customer_latitude', '!=', 0.0),
            ('customer_longitude', '!=', 0.0),
        ],
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        ondelete='cascade',
        domain=[
            ('partner_latitude', '!=', 0.0),
            ('partner_longitude', '!=', 0.0),
        ],
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        related='trip_id.user_id',
        string='Salesperson',
    )
    latitude = fields.Float(compute='_compute_geolocalize', string='Latitude')
    longitude = fields.Float(
        compute='_compute_geolocalize', string='Longitude'
    )
    state = fields.Selection(related='trip_id.state')
    distance = fields.Float(digits=(3, 4))
    sequence = fields.Integer(default=10)
    trip_datetime = fields.Datetime(string='Trip date')
    is_visited = fields.Boolean(string='Is Visited?')
    notes = fields.Text(string='Notes')
    tobe_visited = fields.Boolean(string='To be visited?', default=True)

    def action_toogle_visit(self):
        action = self.env.ref(
            'crm_salesperson_trip.action_salesperson_trip_note'
        ).read()[0]
        action['context'] = {
            'default_trip_line_id': self.id,
            'default_note': self.notes,
        }
        return action

    def unlink(self):
        line_done_ids = self.filtered(lambda l: l.state in ('done', 'running'))
        if line_done_ids:
            raise exceptions.UserError(
                _(
                    'You are not allowed to remove trip already done or is in progress'
                )
            )
        return super(CrmSalespersonTripLine, self).unlink()
