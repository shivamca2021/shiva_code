# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.sale_product_configurator.controllers.main import ProductConfiguratorController

class ProductConfiguratorController(ProductConfiguratorController):

    @http.route(['/sale_product_configurator/configure'], type='json', auth="user", methods=['POST'])
    def configure(self, product_template_id, pricelist_id, **kw):
        add_qty = int(kw.get('add_qty', 1))
        product_template = request.env['product.template'].browse(int(product_template_id))
        pricelist = self._get_pricelist(pricelist_id)

        product_combination = False
        attribute_value_ids = set(kw.get('product_template_attribute_value_ids', []))
        attribute_value_ids |= set(kw.get('product_no_variant_attribute_value_ids', []))
        if attribute_value_ids:
            product_combination = request.env['product.template.attribute.value'].browse(attribute_value_ids)

        if pricelist:
            product_template = product_template.with_context(pricelist=pricelist.id,
                                                             partner=request.env.user.partner_id)

        part_ids = set(kw.get('part_ids', []))
        sub_assembly_ids = set(kw.get('sub_assembly_ids', []))
        material_ids = set(kw.get('material_ids', []))
        internal_material_ids = set(kw.get('internal_material_ids', []))
        external_material_ids = set(kw.get('external_material_ids', []))
        species_ids = set(kw.get('species_ids', []))

        return request.env['ir.ui.view']._render_template("sale_product_configurator.configure", {
            'product': product_template,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'product_combination': product_combination,
            'part_ids': part_ids,
            'sub_assembly_ids': sub_assembly_ids,
            'material_ids': material_ids,
            'internal_material_ids': internal_material_ids,
            'external_material_ids': external_material_ids,
            'species_ids': species_ids
        })