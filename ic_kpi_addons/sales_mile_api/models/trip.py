import logging
from datetime import datetime
import base64
from odoo import models, fields, api

log = logging.getLogger(__name__)


class Trip(models.Model):
    _inherit = 'crm.trip'

    def fetch_todays_trips(self, user_id):
        """
        Fetch all the trips scheduled for
        today in planned, inprogress state.
        """
        _r = []

        trips = self.env['crm.trip'].search([('assign_id', '=', user_id)])
        for trip in trips:
            data = {
                'trip_id': trip.id,
                'name': trip.name,
                'assinged_user': trip.assign_id.name,
                'state': trip.state,
                'Schedule_date': trip.schedule_date,
            }
            _r.append(data)
        return _r

    def get_trip_info(self, tid):
        """Returns the trip information."""
        trip = self.env['crm.trip'].search([('id', '=', int(tid))])
        if len(trip) == 0:
            return False
        # types = [(t.id, t.name) for t in self.env['mail.activity.type'].search([('active', '=', True)])]
        types = []
        data = {
            'trip_id': trip.id,
            'name': trip.name,
            'assigned_user': trip.assign_id.name,
            'state': trip.state,
            'types': types,
            'schedule_date': trip.schedule_date,
            'leads': []
        }
        for cust in trip.crm_trip_line:
            data['leads'].append({
                'name': cust.partner_name,
                'contact_name': cust.contact_name,
                'email': cust.email_from,
                'lat': cust.partner_latitude,
                'long': cust.partner_longitude,
                'sequence': cust.sequence,
                'state': cust.state,
                'remark': cust.remark
            })
        return data

    def get_leads_info(self, tid):
        """Returns the trip information."""
        real_data = []
        lead = self.env['crm.trip'].search([('id', '=', int(tid))])
        if len(lead) == 0:
            return real_data
        # types = [(t.id, t.name) for t in self.env['mail.activity.type'].search([('active', '=', True)])]

        for line in lead.crm_trip_line:

            data = {
                'lead_id': line.id,
                'name': line.name,
                'contact_name': line.contact_name,
                'mail': line.email_from,
                'number': line.phone,
                'note': line.remark,
            }
            real_data.append(data)
        return real_data

    def get_leads_activity(self, tid):
        """Returns the leads information."""
        leads = self.env['crm.trip'].search([('id', '=', int(tid))])
        if len(leads) == 0:
            return False
        types = [(t.id, t.name) for t in self.env['mail.activity.type'].search([('active', '=', True)])]
        data = {
            'types': types
        }
        return data

    def start_trip(self, tid):
        """Change the status of trip to start."""
        trip = self.env['crm.trip'].search([('id', '=', int(tid))])
        print("lead", trip)
        if len(trip) == 0:
            return False
        trip.write({
            'state': 'inprogress'
        })
        return True

    def end_trip(self, tid):
        """Chnage the status as completed of trip."""
        trip = self.env['crm.trip'].search([('id', '=', int(tid))])
        if len(trip) == 0:
            return False
        trip.write({
            'state': 'complete'
        })
        return True

    def cancel_trip(self, tid):
        """Mark cancelled trip."""
        trip = self.env['crm.trip'].search([('id', '=', int(tid))])
        if len(trip) == 0:
            return False
        trip.write({
            'state': 'cancel'
        })
        return True

    def cancel_meet(self, tid, cid):
        """Mark meeting cancelled with client"""
        today = datetime.now().date()
        trip = self.env['crm.trip'].search([
            ('id', '=', int(tid)),
            ('state', '=', 'inprogress'),
            ('schedule_date', '=', today)
        ])
        if len(trip) == 0:
            return False
        cust = trip.crm_trip_line.search([('id', '=', int(cid))])
        if len(cust) == 0:
            return False
        cust.state = 'cancel'
        return True

    def reached_meet(self, tid, cid):
        """Marked the status of meeting as reached
         when sales person reached to the client location."""
        today = datetime.now().date()
        trip = self.env['crm.trip'].search([
            ('id', '=', int(tid)),
            ('state', '=', 'inprogress'),
            ('schedule_date', '=', today)
        ])
        if len(trip) == 0:
            return False
        cust = trip.crm_trip_line.search([('id', '=', int(cid))])
        if len(cust) == 0:
            return False
        cust.state = 'reached'
        return True

    def start_meet(self, tid, cid):
        """Start the meeting."""
        today = datetime.now().date()
        trip = self.env['crm.trip'].search([
            ('id', '=', int(tid)),
            ('state', '=', 'inprogress'),
            ('schedule_date', '=', today)
        ])
        if len(trip) == 0:
            return False
        cust = trip.crm_trip_line.search([('id', '=', int(cid))])
        if len(cust) == 0:
            return False
        cust.state = 'inprogress'
        return True

    def _add_attachments(self, cid, attachs):
        attachment_obj = self.env['ir.attachment']
        lead = self.env['crm.lead'].browse(int(cid))
        for attach in attachs:
            attachment_obj.create({
                'name': lead.name,
                'type': 'binary',
                'datas': base64.b64encode(attach.encode('utf-8')),
                'res_model': 'crm.trip',
                'res_id': int(cid)
            })
        return True

    def _add_note(self, cid, note):
        msg_obj = self.env['mail.message']
        msg_obj.create({
            'type': 'comment',
            'model': 'crm.trip',
            'res_id': int(cid),
            'body': note
        })
        return True

    def _add_activity(self, cid, activity):
        act_obj = self.env['mail.activity']
        act_obj.create({
            'activity_type_id': activity.get('type_id'),
            'date_deadline': activity.get('deadline'),
            'res_model_id': self.env['ir.model'].search([('model', '=', 'crm.lead')], limit=1).id,
            'res_id': activity.get('customer_id'),
            'summary': activity.get('summary'),
            'user_id': activity.get('user_id'),
            'note': activity.get('note'),
        })
        return True

    def completed_meet(self, paylaod):
        """Mark meeting as complated and update the 
        meeting details into respective meeting object."""
        today = datetime.now().date()
        tid = paylaod.get('trip_id')
        cid = paylaod.get('customer_id')
        trip = self.env['crm.trip'].search([
            ('id', '=', int(tid)),
            ('state', '=', 'inprogress'),
            ('schedule_date', '=', today)
        ])
        if len(trip) == 0:
            return False
        cust = trip.crm_trip_line.search([('id', '=', int(cid))])
        if len(cust) == 0:
            return False
        # add meeting feedback
        if paylaod.get('pictures'):
            self._add_attachments(cid, paylaod.get('pictures'))
        if paylaod.get('note'):
            self._add_note(cid, paylaod.get('note'))
        if paylaod.get('activity'):
            self._add_activity(cid, paylaod.get('activity'))

        cust.state = 'complete'
        return True
