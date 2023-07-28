from odoo import fields, models, api, _
import os

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    delivery_package_id = fields.Many2one('product.packaging', 'Delivery Package')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    ribbon_message = fields.Text(compute='_compute_ribbon_message', string='Ribbon Message')
    ribbon_message_red = fields.Text(compute='_compute_ribbon_message', string='Ribbon Message Red')
    
    @api.depends('move_line_ids_without_package.delivery_package_id','move_line_ids_without_package.qty_done','move_line_ids_without_package.product_id')
    def _compute_ribbon_message(self):
        for each in self:
            ribbon_message = ""
            ribbon_message_red = ""
            flag = 1
            red_flag = 1
            pp_ids = each.move_line_ids_without_package.mapped('delivery_package_id')
            for ppd_id in pp_ids:
                all_product_volume = 0
                for line in each.move_line_ids_without_package:
                    if line.delivery_package_id == ppd_id:
                        all_product_volume += (line.product_id.volume * line.qty_done)
                delivery_percentage = all_product_volume / ppd_id.packaging_volume * 100
                if delivery_percentage > 100:
                    red_flag = 0
                    ribbon_message_red = f"{ribbon_message_red} {ppd_id.name} is overfilled {round(delivery_percentage,2)} %. \n"
                else:
                    flag = 0
                    ribbon_message = f"{ribbon_message} {ppd_id.name} : {round(delivery_percentage,2)} % full. \n"
            if flag == 0:
                each.ribbon_message = ribbon_message
            else:
                each.ribbon_message = False

            if red_flag == 0:
                each.ribbon_message_red = ribbon_message_red
            else:
                each.ribbon_message_red = False

