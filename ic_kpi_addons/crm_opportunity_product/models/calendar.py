from odoo import api, fields, models, _

class CalendarEventInherit(models.Model):
    _inherit = 'calendar.event'

    meeting_type = fields.Selection([('personal', 'Personal'), ('company', 'Company')], 'Meeting Type')

    @api.onchange('meeting_type')
    def _onchange_meeting_type(self):
        for record in self:
            if record.name and record.meeting_type == 'personal' and not "P-" in record.name:
                record.name = record.name.strip("C-")
                record.name= "P-" + record.name
            elif record.name and record.meeting_type == 'company' and not "C-" in record.name:
                record.name = record.name.strip("P-")
                record.name = "C-" + record.name
            else:
                if record.name and not record.meeting_type:
                    record.name =record.name.strip("P-C-")

    @api.model
    def create(self, vals):
        record = super(CalendarEventInherit, self).create(vals)
        if record.name and record.meeting_type == 'personal' and not "P-" in record.name:
            record.name = record.name.strip("C-")
            record.name = "P-" + record.name
        elif record.name and record.meeting_type == 'company' and not "C-" in record.name:
            record.name = record.name.strip("P-")
            record.name = "C-" + record.name
        else:
            if record.name and not record.meeting_type:
                record.name = record.name.strip("P-C-")
        return record


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    def add_salesperson(self):
        wizard_form = self.env.ref('crm_opportunity_product.add_saleperson_contact_wizard', False)
        return {
            'name': _('Add Salesperson to select contacts'),
            'type': 'ir.actions.act_window',
            'res_model': 'salesperson.wizard',
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
        }