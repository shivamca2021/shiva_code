from odoo import models, fields, api, _


#
# class SaleOrderInherit(models.Model):
#     _inherit = 'sale.order'
#     _description = 'Adding BOM kit product based on Sale order line Product '
#
#     @api.onchange('order_line')
#     def on_change_bom_product_sale(self):
#         for line in self.order_line:
#             bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'phantom')])
#             for rec in bom.bom_line_ids:
#                 self.update({
#                     'order_line': [
#                         (0, 0, {
#                             'product_id': rec.product_id.product_tmpl_id.id,
#                             'product_qty': rec.product_qty * line.product_uom_qty
#                         })]
#                 })

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    kit_available = fields.Boolean('Bom Kit Availabe', default=False)

    @api.onchange('product_id')
    def on_change_bom_product_sale(self):
        for line in self:
            bom = self.env['mrp.bom'].search(
                [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'phantom')])
            if bom.type == 'phantom':
                self.kit_available = True

    # @api.onchange('product_id')
    def add_bom_kit_component(self):
        for line in self:
            # print(line.product_id.product_tmpl_id.id, '************************')
            bom = self.env['mrp.bom'].search(
                [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'phantom')])
            if bom:
                # Optimization
                # name = ','.join([comp.product_id.name for comp in bom.bom_line_ids])
                # print()
                seq = line.sequence
                for comp in bom.bom_line_ids:
                    self.env['sale.order.line'].create({
                        'sequence': seq,
                        'name': comp.product_id.name + '\t' + 'QTY :\t ' + str(line.product_uom_qty * comp.product_qty),
                        'display_type': 'line_section',
                        'order_id': line.order_id.id,
                    })
                    # 'sequence': seq,
                    # seq = seq+1

                    # if line.product_id == 0:
                    #     comp.unlink()

    def unlink(self):
        for line in self:
            bom = self.env['mrp.bom'].search(
                [('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'phantom')])
            print('*******************************affff')
            return super(SaleOrderLineInherit, self).unlink(bom.bom_line_ids)
                # if line.product_id.prism_bom_id.type == 'phantom':


            # return super(SaleOrderLineInherit, self).unlink()

        # for rec in bom.bom_line_ids:
        #     self.create({
        #         'product_id': rec.product_id.product_tmpl_id.id,
        #         'product_qty': rec.product_qty
        #         # * line.product_qty
        #         # 'product_uom': rec.product_uom_id
        #     })
        #
        # print("************************************ SHOW COMPONENT", bom)

    # def create(self, vals_list):
    #     records = super(IrConfigParameter, self).create(vals_list)
    #     if any(record.key == "crm.pls_fields" for record in records):
    #         self.flush()
    #         self.env.registry.setup_models(self.env.cr)
    #     return records
    #
    # def unlink(self):
    #     pls_emptied = any(record.key == "crm.pls_fields" for record in self)
    #     result = super(IrConfigParameter, self).unlink()
    #     if pls_emptied:
    #         self.flush()
    #         self.env.registry.setup_models(self.env.cr)
    #     return pls_emptied

    # for rec in bom.bom_line_ids:

    #     self.create({
    #         'product_id': rec.product_id.product_tmpl_id.id,
    #         'product_qty': rec.product_qty
    #                        # * line.product_qty
    #         # 'product_uom': rec.product_uom_id
    #     })
