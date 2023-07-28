from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

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

    def button_update_netsuite(self):
        return {
            'type':'ir.actions.act_url',
            'url':'http://3.222.33.74:8001/api/hallmark/a5fx527oyi9b2eta'
        }

    def _create_picking(self):
        res = super(PurchaseOrder, self)._create_picking()
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
        res = super(PurchaseOrder, self).write(line_values)
        self._reset_sequence()
        return res

    def copy(self, default=None):
        return super(PurchaseOrder, self.with_context(keep_line_sequence=True)).copy(
            default
        )

    def cron_update_sequence_existing(self):
        sale_order_id = self.env['sale.order'].sudo().search([])
        purchase_ids = self.sudo().search([])
        for order in sale_order_id:
            count = 1
            for line in order.order_line:
                line.write({'sequence':count})
                count = count+1
        for order in purchase_ids:
            count = 1
            for line in order.order_line:
                line.write({'sequence':count})
                count = count+1


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    _order = "sequence, id"

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

    def _get_product_purchase_description(self, product_lang):
        self.ensure_one()
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase
        bom_ids = self.env["mrp.bom"].search([("product_tmpl_id","=", product_lang.product_tmpl_id.id)])
        if bom_ids:
            bom_dict={name:"\n	"}
            for bom_id in bom_ids:
                for line in bom_id.bom_line_ids:
                    bom_dict.update({line.product_id.name:str(line.product_qty) + " " + str(line.product_uom_id.name)})
            bom_desc = '\n'.join("{}: {}".format(k, v) for k, v in bom_dict.items())
            name = bom_desc
        return name

    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for move, line in zip(res, self):
            move.update(sequence=line.sequence)
        return res

    @api.model
    def create(self, values):
        line = super(PurchaseOrderLine, self).create(values)
        # We do not reset the sequence when copying an entire purchase order
        if not self.env.context.get("keep_line_sequence"):
            line.order_id._reset_sequence()
        if line.sale_line_id:
            line.name = line.sale_line_id.name
        return line

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        res = super(PurchaseOrderLine, self)._onchange_quantity()
        if self.product_qty > 1:
            name = self.product_id.display_name
            bom_ids = self.env["mrp.bom"].search([("product_tmpl_id","=", self.product_id.product_tmpl_id.id)])
            if bom_ids:
                bom_dict={name:"\n	"}
                for bom_id in bom_ids:
                    for line in bom_id.bom_line_ids:
                        bom_dict.update({line.product_id.name:str(line.product_qty * self.product_qty) + " " + str(line.product_uom_id.name)})
                bom_desc = '\n'.join("{}: {}".format(k, v) for k, v in bom_dict.items())
                name = bom_desc
                self.name = name


    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        self.ensure_one()
        self._check_orderpoint_picking_type()
        product = self.product_id.with_context(lang=self.order_id.dest_address_id.lang or self.env.user.lang)
        description_picking = self.name if self.name else product._get_description(self.order_id.picking_type_id)
        if self.product_description_variants:
            description_picking += "\n" + self.product_description_variants
        date_planned = self.date_planned or self.order_id.date_planned
        return {
            # truncate to 2000 to avoid triggering index limit error
            # TODO: remove index in master?
            'name': (self.name or '')[:2000],
            'product_id': self.product_id.id,
            'date': date_planned,
            'date_deadline': date_planned + relativedelta(days=self.order_id.company_id.po_lead),
            'location_id': self.order_id.partner_id.property_stock_supplier.id,
            'location_dest_id': (self.orderpoint_id and not (self.move_ids | self.move_dest_ids)) and self.orderpoint_id.location_id.id or self.order_id._get_destination_location(),
            'picking_id': picking.id,
            'partner_id': self.order_id.dest_address_id.id,
            'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
            'state': 'draft',
            'purchase_line_id': self.id,
            'company_id': self.order_id.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': self.order_id.picking_type_id.id,
            'group_id': self.order_id.group_id.id,
            'origin': self.order_id.name,
            'description_picking': description_picking,
            'propagate_cancel': self.propagate_cancel,
            'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
            'product_uom_qty': product_uom_qty,
            'product_uom': product_uom.id,
        }