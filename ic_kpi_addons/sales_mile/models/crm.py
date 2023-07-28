from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Crm(models.Model):
    _inherit = 'crm.lead'
    _desc = 'CRM'

    date_localization = fields.Date()
    partner_latitude = fields.Float()
    partner_longitude = fields.Float()
    trip_id = fields.Many2one('crm.trip', 'Sales Trip')
    sequence = fields.Integer('Sequence')
    state = fields.Selection([('draft', 'Draft'),
                              ('inprogress', 'Inprogress'),
                              ('reached', 'Reached'),
                              ('complete', 'Completed'),
                              ('cancel', 'Cancel')], default='draft')
    remark = fields.Char('Remark')

    def geo_localize(self):
        # We need country names in English below
        for crm in self.with_context(lang='en_US'):
            result = False
            if not crm.partner_id:
                raise ValidationError(_('Please select Customer first'))
            if crm.partner_id and crm.partner_id.state_id and crm.partner_id.country_id \
                    and crm.partner_id.zip:
                result = crm.partner_id._geo_localize(crm.partner_id.street,
                                                      crm.partner_id.zip,
                                                      crm.partner_id.city,
                                                      crm.partner_id.state_id.name,
                                                      crm.partner_id.country_id.name)
            else:
                if crm.street and crm.zip and crm.city and crm.state_id and crm.country_id:
                    result = crm.partner_id._geo_localize(crm.street,
                                                          crm.zip,
                                                          crm.city,
                                                          crm.state_id.name,
                                                          crm.country_id.name)

            if result:
                crm.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1],
                    'date_localization': fields.Date.context_today(crm)
                })
        return True
