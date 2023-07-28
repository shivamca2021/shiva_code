from odoo import api, fields, models, _

class ProductConfigurationWizard(models.TransientModel):
    _name = 'product.configuration.wizard'

    part_id = fields.Many2one('parts', 'Part')
    part_size = fields.Selection([('link_to_the_object', 'Link to the object'), ('fixed', 'Fixed')], 'Part Size')
    width_size = fields.Selection([('fixed_size', 'Fixed Size'), ('related_to_object', 'Related to Object')],
                                  'Width Size')
    width_fixed = fields.Char('Width')
    width = fields.Char('Width')
    height = fields.Char('Height', default='Material Thickness')
    length_size = fields.Selection([('fixed_size', 'Fixed Size'), ('related_to_object', 'Related to Object')],
                                   'Length Size')
    length_fixed = fields.Char('Length')
    length = fields.Char('Length', default='Length of Related Object - Material Thickness * 2')

    @api.onchange('width_size')
    def onchange_width_size(self):
        if self.width_size == 'related_to_object':
            self.width = 'Width of Related Object - Material Thickness * 2'
        else:
            self.width = ''

    @api.onchange('length_size')
    def onchange_length_size(self):
        if self.length_size == 'related_to_object':
            self.length = 'Length of Related Object - Material Thickness * 2'
        else:
            self.length = ''

    def action_configuration_part_line(self):
        for record in self:
            parts_id=self.env['parts'].sudo().browse(self.env.context.get('active_id'))
            parts_id.write({'part_size': record.part_size,
                                  'width_size': record.width_size,
                                  'length_size': record.length_size,
                                  'width': record.width_fixed or record.width,
                                  'height': record.height,
                                  'length': record.length_fixed or record.length})
