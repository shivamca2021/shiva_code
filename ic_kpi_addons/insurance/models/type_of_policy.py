from odoo import api, fields, models, _

class TypeOfPolicy(models.Model):
    _name = "type.of.policy"
    _description = 'Type of Policy'

    name = fields.Char('Name')