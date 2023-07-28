from odoo import fields, models, api, _


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    def _get_default_volume_uom(self):
        return self.env['product.template']._get_volume_uom_name_from_ir_config_parameter()

    def _compute_volume_uom_name(self):
        for packaging in self:
            packaging.volume_uom_name = self.env['product.template']._get_volume_uom_name_from_ir_config_parameter()

    # packaging_width = fields.Char('Packaging Width')
    # packaging_height = fields.Char('Packaging Height')
    # packaging_length = fields.Char('Packaging Length')
    packaging_volume = fields.Float('Volume')
    volume_uom_name = fields.Char(string='Volume unit of measure label', compute='_compute_volume_uom_name',
                                  default=_get_default_volume_uom)
    height = fields.Float('Height')
    width = fields.Float('Width')
    packaging_length = fields.Float('Length')



    @api.onchange('height', 'width', 'packaging_length')
    def _onchange_volumne(self):
        if self.height and self.width and self.packaging_length:
            self.packaging_volume = (self.height * self.width * self.packaging_length)
        else:
            self.packaging_volume = 0
