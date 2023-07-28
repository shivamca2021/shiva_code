from odoo import api, fields, models, _

class Insurance(models.Model):
    _name = "insurance.details"
    _description = 'Insurance Details'
    _rec_name = 'carrier'

    name = fields.Char('Carrier')
    carrier = fields.Char('Carrier')
    type_of_policy_id = fields.Many2one('type.of.policy', string="Type of Policy")
    partner_id = fields.Many2one('res.partner', string="Insurance Holder")
    insurance_holder_id = fields.Many2one('res.partner', string="Insurance Holder")
    carrier_street = fields.Char()
    carrier_street2 = fields.Char()
    carrier_zip = fields.Char(change_default=True)
    carrier_city = fields.Char()
    carrier_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', carrier_country_id)]")
    carrier_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    
    carrier_name = fields.Char()
    carrier_phone = fields.Char()
    website  = fields.Char()
    broker_street = fields.Char()
    broker_street2 = fields.Char()
    broker_zip = fields.Char(change_default=True)
    broker_city = fields.Char()
    broker_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', broker_country_id)]")
    broker_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    
    broker_name = fields.Char()
    broker_phone = fields.Char()
    email = fields.Char()
    
    
    annual_premium = fields.Float(string='Annual Premium')
    premium_paid = fields.Selection([
        ('monthly','Monthly'),
        ('semi_annually','Semi Annually'),('annually','Annually')], string="Premium Paid", tracking=True)
    
    coverage_date = fields.Date('Dates of Coverage')
    policy_expire_date = fields.Date('Policy Expire Date')
    hard_copy = fields.Binary(string='File')
    hard_copy_filename = fields.Char("Filename")
    
    move_id = fields.Many2one('account.move',string='Invoice')
    payment_state = fields.Selection(related='move_id.payment_state', store=True, string="Payment Status")
    
    state = fields.Selection([
        ('draft','New Policy'),
        ('pending','Pending'),
        ('active','Active'),
        ('claim','Claimed'),
        ('renewed','Renewed'),
        ('expire','Expired'),
        ('cancel','Canceled')], string="Policy Status", default='draft', tracking=True)
    coverage  = fields.Char()

    @api.onchange('insurance_holder_id')
    def insurance_holder_change(self):
        if self.insurance_holder_id:
            self.partner_id = self.insurance_holder_id.id
    