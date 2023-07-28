from odoo import api, fields, models, _

class Partner(models.Model):
    _inherit = "res.partner"
    
    insurance_id = fields.One2many('insurance.details', 'partner_id', string="Insurance Details")