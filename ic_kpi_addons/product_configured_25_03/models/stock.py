# -*- coding: utf-8 -*-
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class StockMove(models.Model):
    _inherit = 'stock.move'

    width = fields.Float('Width', digits='Standard Dimension')
    height = fields.Float('Height', digits='Standard Dimension')
    depth = fields.Float('Depth', digits='Standard Dimension')
    standard_dimension_id = fields.Many2one("standard.dimension", string="Standard Dimension")


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):
        move_values = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id,
                                                                    name, origin, company_id,
                                                                    values)
        sale_line_id = self.env['sale.order.line'].sudo().browse(values.get('sale_line_id'))
        move_values.update({'standard_dimension_id': sale_line_id.standard_dimension_id.id,
                            'width': sale_line_id.width,
                            'height': sale_line_id.height,
                            'depth': sale_line_id.depth})
        return move_values


    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom):
        mo_values = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, company_id, values, bom)
        if mo_values and origin and origin.startswith("S0"):
            mo_values.update({'sale_line_id': values['move_dest_ids'][0].sale_line_id if origin.startswith("S0") else ''})
        return mo_values

