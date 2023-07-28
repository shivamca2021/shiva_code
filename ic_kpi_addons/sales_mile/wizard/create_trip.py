from odoo import models, fields, _
from odoo.exceptions import ValidationError


class TripWz(models.TransientModel):
    _name = 'create.trip.wz'

    date = fields.Date(string='Schedule Date', required=True)

    def create_tip(self):
        crm_ids = self.env['crm.lead'].browse(
            self._context.get('active_ids', []))
        if not crm_ids:
            raise ValidationError(_('Please select at least one lead'))
        if any(crm.trip_id for crm in crm_ids):
            raise ValidationError(_('Selected Lead is already linked with sales trip remove that and then create'))
        sales_person = crm_ids[0].user_id
        if any(crm.user_id != sales_person for crm in crm_ids):
            raise ValidationError(_('please select leads of only one sale person'))
        trip_id = self.env['crm.trip'].create(
            {'state': 'draft', 'schedule_date': self.date, 'assign_id': sales_person.id})
        count = 0
        for crm in crm_ids:
            count += 1
            crm.sequence = count
            crm.trip_id = trip_id.id
