from odoo import models, fields, api


class TripCrm(models.Model):
    _name = 'crm.trip'
    _description = 'Sales Trip'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', copy=False, tracking=True)
    crm_trip_line = fields.One2many('crm.lead', 'trip_id')
    user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user)
    date = fields.Date('Date', default=fields.Date.context_today)
    assign_id = fields.Many2one('res.users', 'Assigned Sales Trip', tracking=True, ondelete='cascade')
    schedule_date = fields.Date('Schedule Date', tracking=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('inprogress', 'In Progress'),
                              ('complete', 'Completed'),
                              ('cancel', 'Cancel')], default='draft', tracking=True)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence']
        vals['name'] = seq.next_by_code(
            'crm.trip.seq') or '/'
        res = super(TripCrm, self).create(vals)
        return res

    def action_inprogress(self):
        self.write({'state': 'inprogress'})

    def action_confirm(self):
        self.write({'state': 'complete'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def location_update(self, post):
        trip_id = post.get('trip_id')
        customer_id = post.get('customer_id')

        crm = self.env['crm.lead'].browse(customer_id)
        if not crm:
            return False
        crm.write({
            'partner_latitude': post.get('latitude'),
            'partner_longitude': post.get('longitude'),
            'date_localization': fields.Date.context_today(crm)
        })
        return True
