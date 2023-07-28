from odoo import fields, models, api


class SaleTemplate(models.Model):
    _name = 'sale.template'

    name = fields.Char()
    sale_template_line_ids = fields.One2many('sale.template.line', 'sale_template_id')


class SaleTemplateLine(models.Model):
    _name = 'sale.template.line'

    sale_template_id = fields.Many2one('sale.template')
    column = fields.Char(string="Column")
    field_id = fields.Many2one('ir.model.fields', string="Field")
