from odoo import fields, models, api, _


class FormulaVariable(models.Model):
    _name = 'formula.variable'
    _description = 'Formula Variable'


    name = fields.Char('Name')
    abbreviation = fields.Char('Abbreviation')
    is_fixed_size = fields.Boolean(string="Is Fixed Size Textbox?", default=False)
    product_group = fields.Selection([('catelog', 'Catalog Product'),
                                      ('parts', 'Parts'),
                                      ('sub_assembly', 'Sub Assembly'),
                                      ('coil_stock', 'Coil Stock'),
                                      ('sheet_stock', 'Sheet Stock'),
                                      ('hardwood', 'Hardwood'),
                                      ('accessories', 'Accessories'),
                                      ('veneer', 'Veneer'),
                                      ('edge_banding', 'Edge Banding'),
                                      ('species', 'Species'),
                                      ('drawer_hardware', 'Drawer Hardware'),
                                      ('door_hardware', 'Door Hardware'),
                                      ('hardware', 'Hardware'),
                                      ('internal_material', 'Internal Material'),
                                      ('external_material', 'External Material'),
                                      ('miscellanies', 'Miscellanies')],
                                     required=True, default='catelog', string="Product Group")
    product_template_field_id = fields.Many2one('ir.model.fields', 'Product Template Fields')