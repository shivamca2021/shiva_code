from odoo import models, fields, api, _
from datetime import timedelta


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    date_planned = fields.Datetime(string='ETA', index=True, copy=False, compute='_compute_date_planned', store=True,
                                   readonly=False,
                                   help="Delivery date promised by vendor. This date is used to determine expected arrival of products.")
    etd = fields.Datetime('ETD', help="Estimated Time of Departure")
    etp = fields.Datetime('ETP', help="Estimated Time of Arrival at Port")
    po_customer_ref = fields.Char('Customer Reference', compute='_compute_purchase_container_number')
    purchase_container_number = fields.Char(compute='_compute_purchase_container_number', string='Container Number')
    cust_po = fields.Char('Customer PO', compute='_compute_purchase_container_number')

    @api.onchange('date_order')
    def _onchange_date_order(self):
        for each in self:
            each.etd = each.date_order + timedelta(days=49)
            each.etp = each.etd + timedelta(days=42)
            each.date_planned = each.etp + timedelta(days=7)
    
    def _compute_purchase_container_number(self):
        for each in self:
            each.po_customer_ref = each.order_line.sale_order_id.client_order_ref
            each.purchase_container_number = each.order_line.sale_order_id.project
            each.cust_po = each.order_line.sale_order_id.customer_po

    def button_confirm(self):
        res = super(PurchaseOrderInherit, self).button_confirm()
        for picking in self.picking_ids:
            picking.eta = self.date_planned
            # picking.receipt_container_number = self.purchase_container_number
            # picking.po_customer_ref = self.po_customer_ref
        return res
