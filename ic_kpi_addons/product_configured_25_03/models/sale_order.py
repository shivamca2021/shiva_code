# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime, timedelta


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    @api.model
    def create(self, values):
        print(self)
        print(values)
        if values.get('sale_line_id'):
            sale_line_id = values.get('sale_line_id')
            if sale_line_id.part_ids or sale_line_id.sub_assembly_ids or sale_line_id.material_ids or sale_line_id.species_ids or sale_line_id.internal_material_ids or sale_line_id.external_material_ids:
                exist_bom_id = self.env['mrp.bom'].sudo().search(
                    [('product_tmpl_id', '=', sale_line_id.product_id.product_tmpl_id.id)])
                parts_list = list(
                    set(sale_line_id.part_ids.ids + sale_line_id.sub_assembly_ids.ids + sale_line_id.material_ids.ids + sale_line_id.species_ids.ids + sale_line_id.internal_material_ids.ids + sale_line_id.external_material_ids.ids))
                bom_id = False
                if exist_bom_id:
                    for record in exist_bom_id:
                        bom_line = record.bom_line_ids.mapped('product_id').ids
                        parts_list.sort(), bom_line.sort()
                        if parts_list == bom_line:
                            bom_id = record
                if not bom_id:
                    bom = {
                        'product_tmpl_id': sale_line_id.product_id.product_tmpl_id.id,
                        'product_id': sale_line_id.product_id.id,
                        'product_qty': 1,
                    }
                    bom_id = self.env['mrp.bom'].sudo().create(bom)
                    bom_lines =[]
                    for parts in sale_line_id.part_ids:
                        vals= (0,0,{'product_id':parts.id})
                        bom_lines.append(vals)
                    for assembly in sale_line_id.sub_assembly_ids:
                        vals = (0, 0, {'product_id': assembly.id})
                        bom_lines.append(vals)
                    for material in sale_line_id.material_ids:
                        vals= (0,0,{'product_id':material.id})
                        bom_lines.append(vals)
                    for species in sale_line_id.species_ids:
                        vals= (0,0,{'product_id':species.id})
                        bom_lines.append(vals)
                    for internal in sale_line_id.internal_material_ids:
                        vals= (0,0,{'product_id':internal.id})
                        bom_lines.append(vals)
                    for external in sale_line_id.external_material_ids:
                        vals= (0,0,{'product_id':external.id})
                        bom_lines.append(vals)
                    bom_id.write({'bom_line_ids':bom_lines})
                if bom_id:
                    values.update({'bom_id':bom_id.id})
                    sale_line_id.write({'prism_bom_id':bom_id.id})
        if values.get('sale_line_id'):
            values.pop('sale_line_id')
        res = super(MrpProduction, self).create(values)
        return res

class Sale(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(Sale, self).action_confirm()
        for line in self.order_line:
            if not line.prism_bom_id and (line.part_ids or line.sub_assembly_ids or line.material_ids or line.species_ids or line.internal_material_ids or line.external_material_ids):
                exist_bom_id = self.env['mrp.bom'].sudo().search([('product_tmpl_id', '=', line.product_id.product_tmpl_id.id)])
                parts_list = list(set(line.part_ids.ids + line.sub_assembly_ids.ids + line.material_ids.ids + line.species_ids.ids + line.internal_material_ids.ids + line.external_material_ids.ids))
                bom_id = False
                if exist_bom_id:
                    for record in exist_bom_id:
                        bom_line = record.bom_line_ids.mapped('product_id').ids
                        parts_list.sort(), bom_line.sort()
                        if parts_list == bom_line:
                            bom_id = record
                if not bom_id:
                    bom = {
                        'product_tmpl_id': line.product_id.product_tmpl_id.id,
                        'product_id': line.product_id.id,
                        'product_qty': 1,
                    }
                    bom_id = self.env['mrp.bom'].sudo().create(bom)
                    bom_lines =[]
                    for parts in line.part_ids:
                        vals= (0,0,{'product_id':parts.id})
                        bom_lines.append(vals)
                    for assembly in line.sub_assembly_ids:
                        vals = (0, 0, {'product_id': assembly.id})
                        bom_lines.append(vals)
                    for material in line.material_ids:
                        vals= (0,0,{'product_id':material.id})
                        bom_lines.append(vals)
                    for species in line.species_ids:
                        vals= (0,0,{'product_id':species.id})
                        bom_lines.append(vals)
                    for internal in line.internal_material_ids:
                        vals= (0,0,{'product_id':internal.id})
                        bom_lines.append(vals)
                    for external in line.external_material_ids:
                        vals= (0,0,{'product_id':external.id})
                        bom_lines.append(vals)
                    bom_id.write({'bom_line_ids':bom_lines})

                # product_id = self.env['product.product'].sudo().search([('product_tmpl_id','=', bom_id.product_tmpl_id.id)])
                mrp_production = self.env['mrp.production'].search(
                    [('product_id', '=', line.product_id.id),
                     ('state', '=', 'draft'),
                     ('bom_id','=', bom_id.id)])
                if not mrp_production:
                    production_vals = {
                        'product_id': line.product_id.id,
                        'bom_id': bom_id.id,
                        'product_qty':1,
                        'product_uom_id': line.product_id.uom_id.id,
                        'origin':line.order_id.name,
                        'date_planned_start': datetime.now(),
                    }
                    mrp_id = self.env['mrp.production'].create(production_vals)
                    if mrp_id.product_id != mrp_id._origin.product_id:
                        mrp_id.move_raw_ids = [(5,)]
                    if mrp_id.bom_id and mrp_id.product_qty > 0:
                        # mrp_id._create_update_move_finished()
                        # keep manual entries
                        list_move_finished = [(4, move.id) for move in mrp_id.move_finished_ids.filtered(
                            lambda m: not m.byproduct_id and m.product_id != mrp_id.product_id)]
                        list_move_finished = []
                        moves_finished_values = mrp_id._get_moves_finished_values()
                        moves_byproduct_dict = {move.byproduct_id.id: move for move in
                                                mrp_id.move_finished_ids.filtered(lambda m: m.byproduct_id)}
                        move_finished = mrp_id.move_finished_ids.filtered(lambda m: m.product_id == mrp_id.product_id)
                        for move_finished_values in moves_finished_values:
                            if move_finished_values.get('byproduct_id') in moves_byproduct_dict:
                                # update existing entries
                                list_move_finished += [(
                                                       1, moves_byproduct_dict[move_finished_values['byproduct_id']].id,
                                                       move_finished_values)]
                            elif move_finished_values.get('product_id') == mrp_id.product_id.id and move_finished:
                                list_move_finished += [(1, move_finished.id, move_finished_values)]
                            else:
                                # add new entries
                                list_move_finished += [(0, 0, move_finished_values)]
                        mrp_id.move_finished_ids = list_move_finished
                        # keep manual entries
                        list_move_raw = [(4, move.id) for move in mrp_id.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
                        moves_raw_values = mrp_id._get_moves_raw_values()
                        move_raw_dict = {move.bom_line_id.id: move for move in
                                         mrp_id.move_raw_ids.filtered(lambda m: m.bom_line_id)}
                        for move_raw_values in moves_raw_values:
                            if move_raw_values['bom_line_id'] in move_raw_dict:
                                # update existing entries
                                list_move_raw += [(1, move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
                            else:
                                # add new entries
                                list_move_raw += [(0, 0, move_raw_values)]
                        mrp_id.move_raw_ids = list_move_raw
                    else:
                        mrp_id.move_raw_ids = [(2, move.id) for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)]

        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    width = fields.Float('Width', digits='Standard Dimension')
    height = fields.Float('Height', digits='Standard Dimension')
    depth = fields.Float('Depth', digits='Standard Dimension')
    product_material_id = fields.Many2one("product.material", string="Product Materials")
    standard_dimension_id = fields.Many2one("standard.dimension", string="Standard Dimension")
    part_ids = fields.Many2many('product.product', 'part_sale_order_line_rel', 'sale_line_id', 'product_id', string="Parts")
    sub_assembly_ids = fields.Many2many('product.product', 'sub_assembly_sale_order_line_rel', 'sale_line_id', 'sub_assembly_product_id', string="Sub Assembly")
    material_ids = fields.Many2many('product.product', 'material_sale_order_line_rel', 'sale_line_id', 'product_id', string="Material Products")
    species_ids = fields.Many2many('product.product', 'species_sale_order_line_rel', 'sale_line_id', 'product_id', string="Species Products")
    internal_material_ids = fields.Many2many('product.product', 'internal_material_sale_order_line_rel', 'sale_line_id', 'product_id',
                                    string="Internal Material Products")
    external_material_ids = fields.Many2many('product.product', 'external_material_sale_order_line_rel', 'sale_line_id',
                                             'product_id',
                                             string="External Material Products")
    prism_bom_id = fields.Many2one('mrp.bom','BOM ID')

    @api.onchange('standard_dimension_id')
    def _onchange_standard_dimension(self):
        if self.standard_dimension_id:
            self.width = self.standard_dimension_id.width
            self.height = self.standard_dimension_id.height
            self.depth = self.standard_dimension_id.depth
        else:
            self.width = 0
            self.height = 0
            self.depth = 0

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res['standard_dimension_id'] = self.standard_dimension_id.id
        res['width'] = self.width
        res['height'] = self.height
        res['depth'] = self.depth
        return res


class SaleProductPartConfigurator(models.TransientModel):
    _name = 'sale.product.part.configurator'

    configured_checkbox = fields.Boolean('Checkbox')
    part_id = fields.Many2one('product.product','Part Name')
    configurator_id = fields.Many2one('sale.product.configurator','Part Name')


class SaleProductSubAssemblyConfigurator(models.TransientModel):
    _name = 'sale.product.sub.assembly.configurator'

    configured_checkbox = fields.Boolean('Checkbox')
    sub_assembly_id = fields.Many2one('product.product','Part Name')
    configurator_id = fields.Many2one('sale.product.configurator','Part Name')


class SaleProductConfiguratorInherit(models.TransientModel):
    _inherit = 'sale.product.configurator'

    part_ids = fields.Many2many('product.product', 'part_sale_product_configure_order_line_rel', 'sale_product_configure_id', 'product_id',
                                string="Parts")
    sub_assembly_ids = fields.Many2many('product.product', 'sub_assembly_sale_product_configure_order_line_rel', 'sale_product_configure_id',
                                        'sub_assembly_product_id', string="Sub Assembly")
    material_ids = fields.Many2many('product.product', 'material_sale_product_configure_order_line_rel', 'sale_product_configure_id', 'material_product_id',
                                    string="Material Products")
    internal_material_ids = fields.Many2many('product.product', 'internal_material_sale_product_configure_order_line_rel',
                                    'sale_product_configure_id', 'internal_material_product_id',
                                    string="Internal Material Products")
    external_material_ids = fields.Many2many('product.product',
                                             'external_material_sale_product_configure_order_line_rel',
                                             'sale_product_configure_id', 'external_material_product_id',
                                             string="External Material Products")
    species_ids = fields.Many2many('product.product', 'species_sale_product_configure_order_line_rel', 'sale_product_configure_id', 'species_product_id',
                                   string="Species Products")
