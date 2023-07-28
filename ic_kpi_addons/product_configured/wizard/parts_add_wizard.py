from odoo import api, fields, models, _

class PartsAddWizard(models.TransientModel):
    _name = 'parts.add.wizard'
    _description = 'Parts Wizard'


    product_id = fields.Many2one("product.template", "product")

    def action_add_parts_in_product(self):
        for record in self:
            part_ids = self.env['product.template'].browse(self.env.context.get('active_ids'))
            value = []
            for rec in part_ids:
                vals = (0, 0, {'name': rec.name,
                               'default_code': rec.default_code,
                               'responsible_id': rec.responsible_id.id,
                               'standard_price': rec.standard_price,
                               'qty_available': rec.qty_available,
                               'uom_id': rec.uom_id.id,
                               'part_id': rec.id,
                               })
                value.append(vals)
            record.product_id.write({'parts_line_ids': value})
            return True

