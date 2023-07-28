from odoo import api, fields, models, _

class DeliveryPackage(models.Model):
    _inherit = 'product.packaging'
    
    height = fields.Float('Height')
    width = fields.Float('Width')
    packaging_length = fields.Float('Length')