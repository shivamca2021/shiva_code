from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends("order_line")
    def _compute_max_line_sequence(self):
        """Allow to know the highest sequence entered in purchase order lines.
        Then we add 1 to this value for the next sequence which is given
        to the context of the o2m field in the view. So when we create a new
        purchase order line, the sequence is automatically max_sequence + 1
        """
        for purchase in self:
            purchase.max_line_sequence = (
                    max(purchase.mapped("order_line.sequence") or [0]) + 1
            )

    max_line_sequence = fields.Integer(
        string="Max sequence in lines", compute="_compute_max_line_sequence"
    )

    def _create_picking(self):
        res = super(SaleOrder, self)._create_picking()
        for order in self:
            if any(
                    [
                        ptype in ["product", "consu"]
                        for ptype in order.order_line.mapped("product_id.type")
                    ]
            ):
                pickings = order.picking_ids.filtered(
                    lambda x: x.state not in ("done", "cancel")
                )
                if pickings:
                    picking = pickings[0]
                    for move, line in zip(
                            sorted(picking.move_lines, key=lambda m: m.id), order.order_line
                    ):
                        move.write({"sequence": line.sequence})
        return res

    def _reset_sequence(self):
        for rec in self:
            current_sequence = 1
            for line in rec.order_line:
                line.sequence = current_sequence
                current_sequence += 1

    def write(self, line_values):
        if line_values.get('name'):
            line_values.update({'so_barcode': line_values.get('name')})
        res = super(SaleOrder, self).write(line_values)
        self._reset_sequence()

        return res

    def copy(self, default=None):
        return super(SaleOrder, self.with_context(keep_line_sequence=True)).copy(
            default
        )

    # project = fields.Char(string='Container No.', default=('T' + str(datetime.now().year)))
    # dt_y = str(datetime.now().year)
    # lst_digit_year = dt_y[2:]
    # default = ('T' + lst_digit_year)
    project = fields.Char(string='Container No.',)
    # Project Name Changed into Container No and Set the Default value

    so_barcode = fields.Char('SO Barcode')

    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['so_barcode']: vals.get('name')
        result = super(SaleOrder, self).create(vals)
        return result

    def button_update_netsuite(self):
        return {
            'type':'ir.actions.act_url',
            'url':'http://3.222.33.74:8001/api/hallmark/kpkyzgpupx5vfbl6'
        }

    def calculate_delivery_package_qty(self):
        for record in self:
            order_lines = record.order_line
            balance_qty = 0.0
            balance_weight = 0.0
            balance_volume = 0.0
            a = []
            for r in order_lines.sorted(lambda m: m.delivery_package_id.id):
                if r.delivery_package_id:
                    if r.delivery_package_id.id in a:
                        balance_qty, balance_weight, balance_volume = r.calculate_container(balance_qty, balance_weight,
                                                                                            balance_volume)
                    else:
                        a.append(r.delivery_package_id.id)
                        balance_qty = 0.0
                        balance_weight = 0.0
                        balance_volume = 0.0
                        balance_qty, balance_weight, balance_volume = r.calculate_container(balance_qty, balance_weight,
                                                                                            balance_volume)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_stock_moves(self, picking):
        res = super(SaleOrderLine, self)._prepare_stock_moves(picking)
        for move, line in zip(res, self):
            move.update(sequence=line.sequence)
        return res

    @api.model
    def create(self, values):
        line = super(SaleOrderLine, self).create(values)
        # We do not reset the sequence when copying an entire purchase order
        if not self.env.context.get("keep_line_sequence"):
            line.order_id._reset_sequence()
        return line

    delivery_package_id = fields.Many2one('product.packaging', 'Delivery Package')
    delivery_package_qty = fields.Float('No. Of Delivery Packaging')
    packaging_qty = fields.Float('Packaging Qty')
    sequence = fields.Integer(
        "Hidden Sequence",
        help="Gives the sequence of the line when " "displaying the purchase order.",
        default=1,
    )

    sequence2 = fields.Integer(
        "Sequence",
        help="Displays the sequence of the line in " "the purchase order.",
        related="sequence",
        readonly=True,
    )

    def calculate_container(self, balance_qty=None, balance_weight=None, balance_volume=None):
        if self.product_id.volume and self.product_id.weight:
            max_container = 1.0
            total_volume = self.product_id.volume * self.product_uom_qty
            total_weight = self.product_id.weight * self.product_uom_qty
            packaging_volume = self.delivery_package_id.packaging_volume + balance_volume
            max_weight = self.delivery_package_id.max_weight + balance_weight
            max_volume_qty = packaging_volume / self.product_id.volume
            max_weight_qty = max_weight / self.product_id.weight
            self.packaging_qty = min(max_volume_qty, max_weight_qty)
            if total_volume > packaging_volume or total_weight > max_weight:
                remaining_qty = self.product_uom_qty - self.packaging_qty
                max_container = max_container + float(
                    str(remaining_qty / self.packaging_qty).split('.')[0])
                decimal_container = str(remaining_qty / self.packaging_qty).split('.')[1]
                if float(decimal_container) > 0.0:
                    max_container = max_container + 1
                    balance_qty = (1.0 - float('0.' + decimal_container)) * self.packaging_qty
                    balance_weight = balance_qty * self.product_id.weight
                    balance_volume = balance_qty * self.product_id.volume
                self.write({'delivery_package_qty': max_container})
            else:
                if balance_weight >= total_weight and balance_volume >= total_volume:
                    max_container = 0.0
                    balance_qty = self.packaging_qty - self.product_uom_qty
                    balance_weight = balance_qty * self.product_id.weight
                    balance_volume = balance_qty * self.product_id.volume
                    self.write({'delivery_package_qty': max_container})
                else:
                    balance_qty = self.packaging_qty - self.product_uom_qty
                    balance_weight = balance_qty * self.product_id.weight
                    balance_volume = balance_qty * self.product_id.volume
                    self.write({'delivery_package_qty': max_container})
        else:
            raise ValidationError(_('volume or weight is not define for the product %s!') % (self.product_id.name))
        return balance_qty, balance_weight, balance_volume

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        name = self.name or self.product_id.name
        bom_ids = self.env["mrp.bom"].search([("product_tmpl_id","=",self.product_template_id.id)])
        if bom_ids:
            bom_dict={name:"\n	"}
            for bom_id in bom_ids:
                for line in bom_id.bom_line_ids:
                    bom_dict.update({line.product_id.name:str(line.product_qty * self.product_uom_qty) + ' '+ str(line.product_uom_id.name)})
            bom_desc = '\n'.join("{}: {}".format(k, v) for k, v in bom_dict.items())
            self.update({'name': bom_desc})

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        name = self.product_id.get_product_multiline_description_sale()
        bom_ids = self.env["mrp.bom"].search([("product_tmpl_id","=",self.product_template_id.id)])
        if bom_ids:
            bom_dict={name:"\n	"}
            for bom_id in bom_ids:
                for line in bom_id.bom_line_ids:
                    bom_dict.update({line.product_id.name:str(line.product_qty * self.product_uom_qty) + ' '+ str(line.product_uom_id.name)})
            bom_desc = '\n'.join("{}: {}".format(k, v) for k, v in bom_dict.items())
            self.update({'name': bom_desc})

    # @api.onchange('delivery_package_id', 'product_id', 'product_uom_qty')
    # def _onchange_delivery_packaging(self):
    #     for record in self:

    # @api.depends('delivery_package_id', 'product_id', 'product_uom_qty')
    # def _compute_containers(self):
    #     for record in self:
    #         if record.delivery_package_id and record.product_id:
    #             same_container_id = self.search([('order_id', '=', record.order_id.ids[0] if len(record.order_id.ids)>=1 else record.order_id.id),
    #                                              ('delivery_package_id', '=', record.delivery_package_id.id)])
    #             balance_qty = 0.0
    #             balance_weight = 0.0
    #             balance_volume = 0.0
    #             for same in same_container_id:
    #                 balance_qty, balance_weight, balance_volume =same.calculate_container(balance_qty,balance_weight,balance_volume)

    # @api.onchange('delivery_package_id','product_id','product_uom_qty')
    # def _onchange_delivery_packaging(self):
    #     for record in self:
    #         if record.delivery_package_id and record.product_id:
    #             if record.product_id.volume or record.product_id.weight:
    #                 total_volume = record.product_id.volume * record.product_uom_qty
    #                 total_weight = record.product_id.weight * record.product_uom_qty
    #                 max_container = 1.0
    #                 if total_volume > record.delivery_package_id.packaging_volume or total_weight > record.delivery_package_id.max_weight:
    #                     max_volume_qty= record.delivery_package_id.packaging_volume/record.product_id.volume
    #                     max_weight_qty=record.delivery_package_id.max_weight/record.product_id.weight
    #                     record.packaging_qty = min(max_volume_qty, max_weight_qty)
    #                     remaining_qty=record.product_uom_qty-record.packaging_qty
    #                     max_container = max_container + float(str(remaining_qty/record.packaging_qty).split('.')[0])
    #                     decimal_container = str(remaining_qty/record.packaging_qty).split('.')[1]
    #                     if float(decimal_container) > 0.0:
    #                         max_container =max_container + 1
    #                     record.delivery_package_qty = max_container
    #
    #                     return
    #                     {
    #
    #                         'warning': {
    #
    #                             'title': 'Warning!',
    #
    #                             'message': 'volume of product is greater then Container volume.'}
    #
    #                     }
    #                 else:
    #                     record.packaging_qty = record.product_uom_qty
    #                     record.delivery_package_qty = max_container
    #             else:
    #                 raise ValidationError(_('volume or weight is not define for the product!'))


class SaleReportInherit(models.Model):
    _inherit = "sale.report"
    _description = "Sales Analysis Report"

    project = fields.Char(string='Container No.', readonly=True)


    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['project'] = ", s.project as project"
        groupby += ', s.project'
        return super(SaleReportInherit, self)._query(with_clause, fields, groupby, from_clause)
