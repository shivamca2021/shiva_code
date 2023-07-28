from odoo import fields, models, api, _


class ProductFields(models.Model):
    _name = 'product.fields'

    name = fields.Char('Name')
