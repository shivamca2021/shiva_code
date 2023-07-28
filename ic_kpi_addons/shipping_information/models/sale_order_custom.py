from odoo import models, fields, api, _
from datetime import timedelta


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    etd = fields.Datetime('ETD', help="Estimated Time of Departure")
    etp = fields.Datetime('ETP', help="Estimated Time of Arrival at Port")


    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        for picking in self.picking_ids:
            picking.etd = self.etd
            picking.state = 'ready_production'
        purchase_order_ids = self._get_purchase_orders()
        for purchase in purchase_order_ids:
            purchase.etd = self.etd
            purchase.etp = self.etp
            purchase.date_planned = self.commitment_date
            purchase.onchange_date_planned()
        return res

    @api.onchange('date_order')
    def _onchange_date_order(self):
        for each in self:
            each.etd = each.date_order + timedelta(days=49)
            each.etp = each.etd + timedelta(days=42)
            each.commitment_date = each.etp + timedelta(days=7) 


class SaleReportInherit(models.Model):
    _inherit = "sale.report"
    _description = "Sales Analysis Report"

    etd = fields.Datetime('ETD', help="Estimated Time of Departure", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['etd'] = ", s.etd as etd"
        groupby += ', s.etd'
        return super(SaleReportInherit, self)._query(with_clause, fields, groupby, from_clause)


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    container_number = fields.Char('Container Number', related='sale_id.project')
    customer_po = fields.Char('Customer PO', related='sale_id.customer_po')
    receipt_container_number = fields.Char('Container Number')
    # container_size = fields.Char('Container Size')
    etd = fields.Datetime('ETD', help="Estimated Time of Departure")
    # ETA for Purchase order
    eta = fields.Datetime('ETA', help="Estimated Time of Arrival")
    container_left_date = fields.Datetime('Container Left Date', help="Date Container left")
    container_received_by_customer_date = fields.Datetime('Container Received at Customer',
                                                          help="Date for Container Received at Customer")
    t_number = fields.Char(string="'T' number")
    # state = fields.Selection(selection_add=[('in_production', 'In Production'),('in_bound', 'In Bound')])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('ready_production', 'Ready for Production'),
        ('in_production', 'In Production'),
        ('assigned', 'Ready'),
        ('confirmed', 'Waiting'),
        ('in_bound', 'In Bound'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * In Production : This transfer is waiting for Production State.\n"
             " * In Bound : This transfer is In bond State.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    def ready(self):
        self.ensure_one()
        self.state = 'assigned'

    def in_production(self):
        self.ensure_one()
        self.state = 'in_production'
        self.show_validate = True

    def delivered(self):
        self.ensure_one()
        self.state = 'done'

    def inbound(self):
        self.ensure_one()
        self.state = 'in_bound'
        self.carrier_tracking_ref = 'INBSHIP'
        # return self.write({'state': 'in_bound'})

    # New Field For Broker Info
    broker_id = fields.Many2one('res.partner', string='Broker Name')
    bill_of_landing_no = fields.Char(string='Bill Of  Landing No.')

    carrier_tracking_ref = fields.Char(string='Tracking Reference', copy=False)
    # Purchase order Customer Reference
    po_customer_ref = fields.Char('Customer Reference', related='sale_id.client_order_ref')
