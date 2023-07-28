from odoo import fields, models, api, _


class FormulaVariable(models.Model):
    _name = 'formula.variable'

    name = fields.Char('Name')
    abbreviation = fields.Char('Abbreviation')
