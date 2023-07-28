# -*- coding: utf-8 -*-

from odoo import api, models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import ValidationError

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    is_default = fields.Boolean('Is Default Value', help="Allow users to set default value")

    @api.model
    def create(self, vals):
        if vals.get('is_default'):
            product_attr_id = self.search([('attribute_id', '=', vals.get('attribute_id')), ('is_default', '=', True)])
            if product_attr_id:
                raise ValidationError(_('You cannot have multiple value as default'))
            product_attr_ids = self.search([('attribute_id', '=', vals.get('attribute_id'))])
            vals['sequence'] = 0
            if product_attr_ids:
                count = 0
                for r in sorted(product_attr_ids, key=lambda k: k['sequence']):
                    count += 1
                    r.write({'sequence': count})

        res = super(ProductAttributeValue, self).create(vals)
        return res

    def write(self, vals):
        for rec in self:
            if vals.get('is_default'):
                product_attr_id = self.search([('attribute_id', '=', rec.attribute_id.id or vals.get('attribute_id')), ('is_default', '=', True), ('id', '!=', rec.id)])
                if product_attr_id:
                    raise ValidationError(_('You cannot have multiple value as default'))
                product_attr_ids = self.search([('attribute_id', '=', rec.attribute_id.id or vals.get('attribute_id')), ('id', '!=', rec.id)])
                vals['sequence'] = 0
                if product_attr_ids:
                    count = 0
                    for r in sorted(product_attr_ids, key=lambda k: k['sequence']):
                        count += 1
                        r.write({'sequence': count})
        return super(ProductAttributeValue, self).write(vals)


