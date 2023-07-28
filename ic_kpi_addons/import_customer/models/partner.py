from odoo import api, fields, models, _

class Partner(models.Model):
    _inherit = "res.partner"
    
    external_id = fields.Integer()
    external_parent_id = fields.Integer('External Parent Id')
    
