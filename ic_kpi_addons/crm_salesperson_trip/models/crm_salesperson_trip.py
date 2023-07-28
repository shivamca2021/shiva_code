# -*- coding: utf-8 -*-
from psycopg2 import sql
from odoo import _, api, exceptions, fields, models


class CrmSalespersonTrip(models.Model):
    _name = 'crm.salesperson.trip'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'CRM Salesperson Trip'
    _rec_name = 'name'

    name = fields.Char()
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        required=True,
        tracking=True,
        default=lambda self: self.env.user,
    )
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', required=True)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('running', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        default='draft',
        tracking=True,
    )
    trip_mode = fields.Selection(
        selection=[
            ('location', 'Location'),
            ('lead_location', 'By Lead/Opportunity'),
            ('contact_location', 'By Contact'),
        ],
        string='Mode',
        default='location',
        required=True,
    )
    location_lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead/Opportunity',
        domain=[
            ('customer_latitude', '!=', 0.0),
            ('customer_longitude', '!=', 0.0),
        ],
    )
    location_contact_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact',
        domain=[
            ('partner_latitude', '!=', 0.0),
            ('partner_longitude', '!=', 0.0),
        ],
    )
    location = fields.Char(string='Location')
    location_latitude = fields.Float(digits=(16, 5))
    location_longitude = fields.Float(digits=(16, 5))
    trip_line = fields.One2many(
        comodel_name='crm.salesperson.trip.line',
        inverse_name='trip_id',
        string='Contacts',
    )
    radius = fields.Float(string='Radius', default=1.0)
    max_contacts = fields.Selection(
        selection=[
            ('10', '10'),
            ('15', '15'),
            ('20', '20'),
            ('30', '30'),
            ('50', '50'),
        ],
        string='Number of records',
        default='10',
        required=True,
        states={'draft': [('readonly', False)]},
    )
    notes = fields.Html(string='Notes')

    _sql_constraints = [
        (
            'visit_period_check',
            'CHECK(start_date <= end_date)',
            'The start date must be anterior to the end date',
        )
    ]

    def action_running(self):
        self.write({'state': 'running'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.onchange('location_lead_id')
    def change_location_lead_id(self):
        if self.location_lead_id:
            self.location_latitude = self.location_lead_id.customer_latitude
            self.location_longitude = self.location_lead_id.customer_longitude

    @api.onchange('location_contact_id')
    def change_location_contact_id(self):
        if self.location_contact_id:
            self.location_latitude = self.location_contact_id.partner_latitude
            self.location_longitude = (
                self.location_contact_id.partner_longitude
            )

    def action_compute_contacts(self):
        self.ensure_one()
        if not self.location_latitude or not self.location_longitude:
            raise exceptions.UserError(_('Geolocation is required!'))

        if not self.max_contacts:
            raise exceptions.UserError(_('Number of contact is required!'))

        latitude = longitude = 0.0
        if self.trip_mode == 'lead_location':
            latitude = self.location_lead_id.customer_latitude
            longitude = self.location_lead_id.customer_longitude
        elif self.trip_mode == 'contact_location':
            latitude = self.location_contact_id.partner_latitude
            longitude = self.location_contact_id.partner_longitude
        else:
            latitude = self.location_latitude
            longitude = self.location_longitude

        contacts = self.get_location_around(
            latitude,
            longitude,
            self.radius,
            self.max_contacts,
            'res_partner',
        )
        leads = self.get_location_around(
            latitude,
            longitude,
            self.radius,
            self.max_contacts,
        )

        line_obj = self.env['crm.salesperson.trip.line']
        line_ids = self.env['crm.salesperson.trip.line']

        self.trip_line = [(6, 0, [])]
        for partner, distance in contacts.items():
            line_ids += line_obj.with_context(
                default_partner_id=partner
            ).create(
                {
                    'trip_id': self.id,
                    'partner_id': partner,
                    'distance': distance,
                    'source_data': 'contact',
                }
            )

        for lead, distance in leads.items():
            line_ids += line_obj.with_context(default_lead_id=lead).create(
                {
                    'trip_id': self.id,
                    'lead_id': lead,
                    'distance': distance,
                    'source_data': 'lead',
                }
            )

        self.trip_line = [(6, 0, line_ids.ids)]

    def get_location_around(
        self, lat, lng, distance, limit=10, source='crm_lead'
    ):
        if source not in ('crm_lead', 'res_partner'):
            raise exceptions.UserError(
                _('Source are not supported. Only crm_lead or res_partner')
            )

        sources = {
            'crm_lead': {
                'table': self.env['crm.lead']._table,
                'latitude': 'customer_latitude',
                'longitude': 'customer_longitude',
            },
            'res_partner': {
                'table': self.env['res.partner']._table,
                'latitude': 'partner_latitude',
                'longitude': 'partner_longitude',
            },
        }

        table = sources[source]['table']
        latitude = sources[source]['latitude']
        longitude = sources[source]['longitude']

        distance_query = """SELECT *
        FROM (
            SELECT id, (point(%s, %s) <@> point({lat}, {lng})) AS distance
            FROM {table}
            WHERE {lat} > 0.0 OR {lng} > 0.0
        ) AS distances
        WHERE distances.distance <= %s
        ORDER BY distance ASC
        LIMIT %s"""

        query = sql.SQL(distance_query).format(
            table=sql.Identifier(table),
            lat=sql.Identifier(latitude),
            lng=sql.Identifier(longitude),
        )
        self.env.cr.execute(query, (lat, lng, distance, limit))
        result = dict(self.env.cr.fetchall())
        return result

    def action_view_contact_google_map(self):
        self.ensure_one()
        action = self.env.ref(
            'crm_salesperson_trip.action_crm_salesperson_trip_line_google_map'
        ).read()[0]
        contacts_to_visit = self.trip_line.filtered(lambda l: l.tobe_visited)
        if not contacts_to_visit:
            raise exceptions.UserError(
                _('You haven\'t defined any contact you want to visit')
            )

        action['domain'] = [('id', 'in', contacts_to_visit.ids)]
        return action

    def unlink(self):
        trip_ids = self.filtered(lambda l: l.state in ('done', 'running'))
        if trip_ids:
            raise exceptions.UserError(
                _(
                    'You are not allowed to remove trip already done or is in progress'
                )
            )
        return super(CrmSalespersonTrip, self).unlink()

    def action_start_travel(self):
        self.ensure_one()
        total_trip = len(self.trip_line)
        if total_trip == 0:
            raise exceptions.UserError(
                _('You must define at least one location')
            )

        google_url = 'https://www.google.com/maps/dir/?api=1&dir_action=navigate&travelmode=driving'
        destination = self.trip_line[-1]
        destination_str = f'{destination.latitude},{destination.longitude}'
        if total_trip > 1:
            waypoints = '|'.join(
                [
                    f'{trip.latitude},{trip.longitude}'
                    for trip in self.trip_line[0 : total_trip - 1]
                ]
            )
            return {
                'type': 'ir.actions.act_url',
                'name': 'Sales trip directions',
                'target': 'new',
                'url': f'{google_url}&waypoints={waypoints}&destination={destination_str}',
            }

        return {
            'type': 'ir.actions.act_url',
            'name': 'Sales trip directions',
            'target': 'new',
            'url': f'{google_url}&destination={destination_str}',
        }
