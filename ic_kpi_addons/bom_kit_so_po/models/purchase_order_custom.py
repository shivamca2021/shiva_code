from odoo import models, fields, api, _


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order.line'

    kit_available = fields.Boolean('Bom Kit Availabe', default=False)

    @api.onchange('product_id')
    def on_change_bom_product_sale(self):
        for line in self:
            bom = self.env['mrp.bom'].search(
                [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'phantom')])
            if bom.type == 'phantom':
                self.kit_available = True

    def add_button_bom_kit_component(self):
        for line in self:
            # print(line.product_id.product_tmpl_id.id, '************************')
            bom = self.env['mrp.bom'].search(
                [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'phantom')])
            if bom:
                seq = line.sequence
                # Optimization
                name = ','.join([comp.product_id.name for comp in bom.bom_line_ids])
                for comp in bom.bom_line_ids:
                    self.env['purchase.order.line'].create({
                        'sequence': seq,
                        'name': comp.product_id.name + '\t' + 'QTY :\t ' + str(comp.product_qty),
                        'display_type': 'line_section',
                        'order_id': line.order_id.id,
                    })

































    # @api.onchange('order_line')
    # def on_change_bom_product(self):
    #     for line in self.order_line:
    #         bom = self.env['mrp.bom'].search(
    #             [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'phantom')])
    #         for rec in bom.bom_line_ids:
    #             self.update({
    #                 'order_line': [
    #                     (0, 0, {
    #                         'product_id': rec.product_id.product_tmpl_id.id,
    #                         'product_qty': rec.product_qty * line.product_qty
    #                     })]
    #             })
    #



    # @api.onchange('order_line')
    # def on_change_bom_product(self):
    #     for line in self.order_line:
    #         bom = self.env['mrp.bom'].search(
    #             [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'phantom')])
    #         for rec in bom.bom_line_ids:
    #             self.update({
    #                 'order_line': [
    #                     (0, 0, {
    #                         'product_id': rec.product_id.product_tmpl_id.id,
    #                         'product_qty': rec.product_qty * line.product_qty
    #                     })]
    #             })
