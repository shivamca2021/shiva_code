# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models
import pytz
import datetime

class DashboardReport(models.Model):
    _name = "dashboard.report"
    _description = "Dashboard Report"
    _auto = False
    _rec_name = 'id'

    @api.depends('so_id', 'po_id', 'mo_id', 'wo_id', 'picking_id', 'shipping_id')
    def _compute_display_name(self):
        qo_days = so_days = mo_days = po_days = shipment_days = wo_days = wo_end_days = picking_days = installment_days = current_state = ''
        operation_days = {}
        todate = datetime.date.today()
        for report_line in self:
            if report_line.so_id:
                qt_days = todate - report_line.quote_date
                operation_days.update({'quote': qt_days.days})
                st_days = todate - report_line.order_date.date()
                operation_days.update({'sale': st_days.days})
                qo_days = report_line.so_id.name + '(' + str(report_line.diff_op_qo_date_int) + ' Days)'
                so_days = str(report_line.so_id.date_order.strftime("%m/%d/%Y")) + '(' + str(report_line.diff_so_qo_date_int) + ' Days)'
            if report_line.mo_id:
                mt_days = todate - report_line.mo_start_date
                operation_days.update({'manufacture': mt_days.days})
                mo_days = report_line.mo_id.name + '(' + str(report_line.diff_so_mo_date_int) + ' Days)'
            if report_line.po_id:
                pt_days = todate - report_line.po_date
                operation_days.update({'purchase': pt_days.days})
                po_days = report_line.po_id.name + '(' + str(report_line.diff_po_mo_date_int) + ' Days)'
            if report_line.shipping_id:
                if report_line.shipping_date:
                    spt_days = todate - report_line.shipping_date
                    operation_days.update({'shipping': spt_days.days})
                shipment_days = report_line.shipping_id.name + '(' + str(report_line.diff_po_incom_ship_date_int) + ' Days)'
            if report_line.wo_id:
                if report_line.wo_date:
                    wt_days = todate - report_line.wo_date
                    operation_days.update({'work-order': wt_days.days})
                wo_days = report_line.wo_id.name + '(' + str(report_line.diff_mos_wos_date_int) + ' Days)'
                if report_line.wo_id.date_planned_finished:
                    wt_end_days = todate - report_line.wo_end_date.date()
                    operation_days.update({'work-order-end': wt_end_days.days})
                    wo_end_days = str(report_line.wo_id.date_planned_finished.strftime("%m/%d/%Y")) + '(' + str(report_line.diff_wos_woe_date_int) + ' Days)'
                else:
                    wo_end_days = ''
            if report_line.picking_id:
                if report_line.picking_date:
                    dt_days = todate - report_line.picking_date
                    operation_days.update({'delivery': dt_days.days})
                picking_days = report_line.picking_id.name + '(' + str(report_line.diff_do_mod_date_int) + ' Days)'
                if report_line.picking_id.installation_date:
                    it_days = todate - report_line.installation_date
                    operation_days.update({'installment': it_days.days})
                    installment_days = str(report_line.picking_id.installation_date.strftime("%m/%d/%Y")) + '(' + str(report_line.diff_do_install_date_int) + ' Days)'
                else:
                    installment_days = ''

            pos_diff = {}
            neg_diff = {}

            for key, value in operation_days.items():
                if value >= 0:
                    pos_diff.update({key: value})
                else:
                    neg_diff.update({key: value})

            if len(pos_diff) > 0:
                min_val = min(pos_diff.values())
                min_res = [key for key in pos_diff if pos_diff[key] == min_val]
                current_state = min_res[0]
            if len(neg_diff) > 0:
                max_val = max(neg_diff.values())
                max_res = [key for key in neg_diff if neg_diff[key] == max_val]
                current_state = max_res[0]
            report_line.update({
                'qo_days': qo_days,
                'so_days': so_days,
                'mo_days': mo_days,
                'po_days': po_days,
                'shipment_days': shipment_days,
                'wo_days': wo_days,
                'wo_end_days': wo_end_days,
                'picking_days': picking_days,
                'installment_days': installment_days,
                'current_state': current_state
            })

    id = fields.Char('ID', readonly=True)
    opportunity_name = fields.Char('Opportunity Reference', readonly=True)
    opportunity_id = fields.Many2one('crm.lead', readonly=True)
    opportunity_date = fields.Date('Opportunity Date', readonly=True)
    so_name = fields.Char('Sale Order', readonly=True)
    so_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    quote_date = fields.Date('Quote Date', readonly=True)
    order_date = fields.Datetime('Order Date', readonly=True)
    po_name = fields.Char('Purchase Order', readonly=True)
    po_id = fields.Many2one('purchase.order', 'Purchase Order', readonly=True)
    po_date = fields.Date('Purchase Date', readonly=True)
    mo_name = fields.Char('Manufacturing Order', readonly=True)
    mo_id = fields.Many2one('mrp.production', readonly=True)
    mo_start_date = fields.Date('Manufacturing Date', readonly=True)
    mo_date = fields.Datetime('Manufacturing Deadline Date', readonly=True)
    wo_name = fields.Char('Work Order Reference', readonly=True)
    wo_id = fields.Many2one('mrp.workorder', readonly=True)
    wo_date = fields.Date('Work Order Start Date', readonly=True)
    wo_end_date = fields.Datetime('Work Order End Date', readonly=True)
    picking_name = fields.Char('Delivery Order', readonly=True)
    picking_id = fields.Many2one('stock.picking', readonly=True)
    diff_so_qo_date = fields.Char('Days From Quote To Sales Order', readonly=True)
    diff_so_qo_date_int = fields.Integer('Days From Quote To Sales Order', readonly=True)
    diff_so_po_date = fields.Char('Days From Sales Order To PO Date', readonly=True)
    diff_so_po_date_int = fields.Integer('Days From Sales Order To PO Date', readonly=True)
    diff_po_mo_date = fields.Char('Days From PO To Manf. start', readonly=True)
    diff_po_mo_date_int = fields.Integer('Days From PO To Manf. start', readonly=True)
    diff_mos_mod_date = fields.Char('Days From Manf. start To Manf deadline', readonly=True)
    diff_mos_mod_date_int = fields.Integer('Days From Manf. start To Manf deadline', readonly=True)
    diff_mos_wos_date = fields.Char('Days From Manf. Start To WO Start', readonly=True)
    diff_mos_wos_date_int = fields.Integer('Days From Manf. Start To WO Start', readonly=True)
    diff_wo_mod_date = fields.Char('Days From WO Start To Manf. Deadline', readonly=True)
    diff_wo_mod_date_int = fields.Integer('Days From WO Start To Manf. Deadline', readonly=True)
    diff_do_mod_date = fields.Char('Manufactured to Delivery Order', readonly=True)
    diff_do_mod_date_int = fields.Integer('Manufactured to Delivery Order', readonly=True)
    diff_so_do_date  = fields.Char('Sale Order to Delivery Order', readonly=True)
    diff_so_do_date_int = fields.Integer('Sale Order to Delivery Order', readonly=True)

    diff_op_qo_date = fields.Char('Days From Opportunity To Quote', readonly=True)
    diff_op_qo_date_int = fields.Integer('Days From Opportunity To Quote', readonly=True)
    diff_so_mo_date = fields.Char('Days From Sales Order To Manf. start', readonly=True)
    diff_so_mo_date_int = fields.Integer('Days From Sales Order To Manf. start', readonly=True)
    diff_mo_po_date = fields.Char('Days From Manf. start To PO', readonly=True)
    diff_mo_po_date_int = fields.Integer('Days From Manf. start To PO', readonly=True)
    diff_wos_woe_date = fields.Char('Days From WO Start To WO End', readonly=True)
    diff_wos_woe_date_int = fields.Integer('Days From WO Start To WO End', readonly=True)
    diff_wos_mod_date = fields.Char('Days From WO Start To Manf deadline', readonly=True)
    diff_wos_mod_date_int = fields.Integer('Days From WO Start To Manf deadline', readonly=True)
    diff_pqo_po_date = fields.Char('Days From Quote To PO', readonly=True)
    diff_pqo_po_date_int = fields.Integer('Days From Quote To PO', readonly=True)
    diff_mo_do_date  = fields.Char('Manf. Start to Delivery Order', readonly=True)
    diff_mo_do_date_int = fields.Integer('Manf. Start to Delivery Order', readonly=True)
    diff_mo_install_date = fields.Char('Days From MO to Installation Date', readonly=True)
    diff_mo_install_date_int = fields.Integer('Days From MO To Installation Date', readonly=True)
    diff_do_install_date_int = fields.Integer('Days From DO To Installation Date', readonly=True)
    diff_po_incom_ship_date  = fields.Char('Days From PO To Incoming Shipment', readonly=True)
    diff_po_incom_ship_date_int = fields.Integer('Days From PO To Incoming Shipment', readonly=True)
    shipping_id = fields.Many2one('stock.picking', readonly=True)
    shipping_name = fields.Char('Shipment Order', readonly=True)
    shipping_date = fields.Date('Shipment Date', readonly=True)
    shipping_status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Shipment Status', readonly=True)
    picking_date = fields.Date('Delivery Date', readonly=True)
    picking_status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Delivery Status', readonly=True)
    installation_date = fields.Datetime('Installation Date', readonly=True)
    invoice_name = fields.Char('Invoice Number', readonly=True)
    invoice_id = fields.Many2one('account.move', readonly=True)
    invoice_date = fields.Datetime('Invoice Due Date', readonly=True)
    qo_days = fields.Char(string="Quotation Days", compute="_compute_display_name")
    so_days = fields.Char(string="Sale Order Days", compute="_compute_display_name")
    mo_days = fields.Char(string="Manufacturing Order Days", compute="_compute_display_name")
    po_days = fields.Char(string="Purchase Order Days", compute="_compute_display_name")
    shipment_days = fields.Char(string="Shipment Order Days", compute="_compute_display_name")
    wo_days = fields.Char(string="Work Order Start Days", compute="_compute_display_name")
    wo_end_days = fields.Char(string="Work Order End Days", compute="_compute_display_name")
    picking_days = fields.Char(string="Delivery Order Days", compute="_compute_display_name")
    installment_days = fields.Char(string="Installment Days", compute="_compute_display_name")
    current_state = fields.Char('Current State', compute="_compute_display_name")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            id,
            opportunity_name,
            case when opportunity_id = 0 then  null else opportunity_id end as opportunity_id,
            opportunity_date,
            so_name,
            so_id,
            quote_date,
            order_date,
            picking_name,
            picking_id,
            picking_status,
            picking_date,
            installation_date,
            invoice_name,
            invoice_id,
            invoice_date,
            mo_name,
            mo_id,
            mo_start_date,
            wo_name,
            wo_id,
            wo_date,
            wo_end_date,
            mo_date,
            po_name,
            po_id,
            date(x.po_order_date) as po_date,
            shipping_id,
            shipping_name,
            shipping_date,
            shipping_status,
            concat(x.order_date::date - x.quote_date::date, ' ', 'Days') as diff_so_qo_date,
            x.order_date::date - x.quote_date::date as diff_so_qo_date_int,
            concat(case when x.po_planned_date::date - x.order_date::date is null then 0 else x.po_planned_date::date - x.order_date::date end , ' ', 'Days') as diff_so_po_date,
            concat(case when x.po_create_date::date - x.mo_start_date::date is null then 0 else x.po_create_date::date - x.mo_start_date::date end, ' ', 'Days') as diff_po_mo_date,
            concat(case when x.mo_date::date - x.mo_start_date::date is null then 0 else x.mo_date::date - x.mo_start_date::date end, ' ', 'Days') as diff_mos_mod_date,
            concat(case when x.wo_date::date - x.mo_start_date::date is null then 0 else x.wo_date::date - x.mo_start_date::date end, ' ', 'Days') as diff_mos_wos_date,
            concat(case when x.mo_date::date - x.wo_date::date is null then 0 else x.mo_date::date - x.wo_date::date end, ' ', 'Days') as diff_wo_mod_date,
            concat(case when x.picking_deadline_date::date - x.mo_date::date is null then 0 else x.picking_deadline_date::date - x.mo_date::date end, ' ', 'Days') as diff_do_mod_date,
            concat(case when x.picking_deadline_date::date - x.order_date::date is null then 0 else x.picking_deadline_date::date - x.order_date::date end, ' ', 'Days') as diff_so_do_date,
            concat(case when x.quote_date::date - x.opportunity_date::date is null then 0 else x.quote_date::date - x.opportunity_date::date end , ' ', 'Days') as diff_op_qo_date,
            concat(case when x.mo_start_date::date - x.order_date::date is null then 0 else x.mo_start_date::date - x.order_date::date end , ' ', 'Days') as diff_so_mo_date,
            concat(case when x.po_planned_date::date - x.mo_start_date::date is null then 0 else x.po_planned_date::date - x.mo_start_date::date end , ' ', 'Days') as diff_mo_po_date,
            concat(case when x.wo_end_date::date - x.wo_date::date is null then 0 else x.wo_end_date::date - x.wo_date::date end , ' ', 'Days') as diff_wos_woe_date,
            concat(case when x.mo_date::date - x.wo_date::date is null then 0 else x.mo_date::date - x.wo_date::date end , ' ', 'Days') as diff_wos_mod_date,
            concat(case when x.po_order_date::date - x.po_planned_date::date is null then 0 else x.po_order_date::date - x.po_planned_date::date end , ' ', 'Days') as diff_pqo_po_date,
            concat(case when x.mo_start_date::date - x.picking_deadline_date::date is null then 0 else x.mo_start_date::date - x.picking_deadline_date::date end, ' ', 'Days') as diff_mo_do_date,
            
            concat(case when x.installation_date::date - x.mo_date::date is null then 0 else x.installation_date::date - x.mo_date::date end, ' ', 'Days') as diff_mo_install_date,
            concat(case when x.shipping_date::date - x.po_order_date::date is null then 0 else x.shipping_date::date - x.po_order_date::date end, ' ', 'Days') as diff_po_incom_ship_date,

            case when x.quote_date::date - x.opportunity_date::date is null then 0 else x.quote_date::date - x.opportunity_date::date end  as diff_op_qo_date_int,
            case when x.mo_start_date::date - x.order_date::date is null then 0 else x.mo_start_date::date - x.order_date::date end as diff_so_mo_date_int,
            
            case when x.po_planned_date::date - x.mo_start_date::date is null then 0 else x.po_planned_date::date - x.mo_start_date::date end as diff_mo_po_date_int,
            case when x.wo_date::date - x.wo_end_date::date is null then 0 else x.wo_date::date - x.wo_end_date::date end  as diff_wos_woe_date_int,
            
            case when x.mo_date::date - x.wo_end_date::date is null then 0 else x.mo_date::date - x.wo_end_date::date end as diff_wos_mod_date_int,
            
            case when x.po_order_date::date - x.po_planned_date::date is null then 0 else x.po_order_date::date - x.po_planned_date::date end as diff_pqo_po_date_int,
            
            
            case when x.mo_start_date::date - x.picking_deadline_date::date is null then 0 else x.mo_start_date::date - x.picking_deadline_date::date end as diff_mo_do_date_int,
            
            case when x.installation_date::date - x.mo_date::date is null then 0 else x.installation_date::date - x.mo_date::date end as diff_mo_install_date_int,
            
            case when x.po_planned_date::date - x.order_date::date is null then 0 else x.po_planned_date::date - x.order_date::date end  as diff_so_po_date_int,
            
            
            case when x.po_order_date::date - x.mo_start_date::date is null then 0 else x.po_order_date::date - x.mo_start_date::date end as diff_po_mo_date_int,
            
            case when x.mo_date::date - x.mo_start_date::date is null then 0 else x.mo_date::date - x.mo_start_date::date end as diff_mos_mod_date_int,
            
            case when x.wo_date::date - x.mo_start_date::date  is null then 0 else x.wo_date::date - x.mo_start_date::date end as diff_mos_wos_date_int,
            
            case when x.mo_date::date - x.wo_date::date is null then 0 else x.mo_date::date - x.wo_date::date end as diff_wo_mod_date_int,
            
            case when x.picking_deadline_date::date - x.mo_date::date is null then 0 else x.picking_deadline_date::date - x.mo_date::date end as diff_do_mod_date_int,
            
            case when x.installation_date::date - x.picking_deadline_date::date is null then 0 else x.installation_date::date - x.picking_deadline_date::date end as diff_do_install_date_int,
            case when x.picking_deadline_date::date - x.order_date::date is null then 0 else x.picking_deadline_date::date - x.order_date::date end as diff_so_do_date_int,
            case when x.shipping_date::date - x.po_order_date::date is null then 0 else x.shipping_date::date - x.po_order_date::date end as diff_po_incom_ship_date_int
            
        """

        # wo.name as wo_name,
        # wo.date_planned_start as wo_date,

        for field in fields.values():
            select_ += field

        # from_ = """crm_lead o join sale_order s ON (o.id=s.opportunity_id)
        from_select_ = """
            max(concat(s.id,'-',p.id,'-',po.id,'-',o.id,'-',wo.id)) as id,        
            max(s.op_name) as opportunity_name,
            max(CAST(coalesce(s.op_id, '0') AS integer)) as opportunity_id,
            max(date(s.op_create_date)) as opportunity_date,
            max(s.name) as so_name,
            max(s.id) as so_id,
            max(date(s.create_date)) as quote_date,
            max(s.date_order) as order_date,
            max(p.name) as picking_name,
            max(p.id) as picking_id,
            max(p.state) as picking_status,
            max(date(p.date_done)) as picking_date,
            max(p.date_deadline) as picking_deadline_date,
            max(p.installation_date) as installation_date,
            max(m.name) as invoice_name,
            max(m.id) as invoice_id,
            max(m.invoice_date) as invoice_date,
            max(o.name) as mo_name,
            max(o.id) as mo_id,
            min(date(o.date_planned_start)) as mo_start_date,
            max(wo.name) as wo_name,
            max(wo.id) as wo_id,
            min(date(wo.date_planned_start)) as wo_date,
            max(wo.date_planned_finished) as wo_end_date,
            max(o.date_deadline) as mo_date,
            max(po.name) as po_name,
            max(po.id) as po_id,
            min(po.date_planned) as po_planned_date,
            max(date(po.date_order)) as po_order_date,
            max(po.create_date) as po_create_date,
            max(ppick.id) as shipping_id,
            max(ppick.name) as shipping_name,
            max(date(ppick.date_done)) as shipping_date,
            max(ppick.state) as shipping_status
        """
        from_ = """(select ss.id,ss.opportunity_id,ss.date_order,ss.create_date,ss.name,op.name as op_name,op.id::text as op_id,
TO_CHAR(op.create_date, 'YYYY-MM-DD HH:MM:SS.US') as op_create_date FROM crm_lead op inner join sale_order ss ON 
(op.id=ss.opportunity_id and op.active=TRUE AND op.type='opportunity' and ss.state in ('sale','done')) 
union 
select so.id, so.opportunity_id,so.date_order,so.create_date,so.name, null,null,null from sale_order as so where so.state in ('sale','done')) as s
        left join stock_picking p ON (p.sale_id=s.id)
        left join account_move m ON (m.invoice_origin ILIKE '%' || s.name || '%')
        left join mrp_production o ON (o.origin ILIKE '%' || s.name || '%')
        left join purchase_order po ON (po.origin ILIKE '%' || o.name || '%')
        left join stock_picking ppick ON (ppick.origin ILIKE '%' || po.name || '%')
        left join mrp_workorder wo ON(o.id = wo.production_id)
        """
        # right join mrp_workorder wo ON(o.id = wo.production_id)
        where_ = """op.active=TRUE AND op.type='opportunity'"""
        # return '%s (SELECT %s FROM %s WHERE %s)' % (with_, select_, from_, where_)
        # return '%s (SELECT %s FROM %s)' % (with_, select_, from_)

        groupby_ = """s.id"""

        orderby_ = """s.id"""

        return '%s (SELECT %s FROM ( SELECT %s FROM %s  GROUP BY %s ORDER BY %s )  AS x)' % (
        with_,select_, from_select_, from_, groupby_, orderby_)

        # o.id as id,
        # o.name as opportunity_name,
        # select_ = """
        # concat(s.id,'-',p.id,'-',po.id,'-',o.id,'-',wo.id) as id,        
        # op.name as opportunity_name,
        # op.id as opportunity_id,
        # op.create_date as opportunity_date,
        # s.name as so_name,
        # s.id as so_id,
        # s.create_date as quote_date,
        # s.date_order as order_date,
        # concat(s.create_date::date - s.date_order::date, ' ', 'Days') as diff_so_qo_date,
        # s.create_date::date - s.date_order::date as diff_so_qo_date_int,
        # concat(case when s.date_order::date - po.date_planned::date is null then 0 else s.date_order::date - po.date_planned::date end , ' ', 'Days') as diff_so_po_date,
        # concat(case when po.date_planned::date - o.date_planned_start::date is null then 0 else po.date_planned::date - o.date_planned_start::date end, ' ', 'Days') as diff_po_mo_date,
        # concat(case when o.date_planned_start::date - o.date_deadline::date is null then 0 else o.date_planned_start::date - o.date_deadline::date end, ' ', 'Days') as diff_mos_mod_date,
        # concat(case when o.date_planned_start::date - wo.date_planned_start::date is null then 0 else o.date_planned_start::date - wo.date_planned_start::date end, ' ', 'Days') as diff_mos_wos_date,
        # concat(case when wo.date_planned_start::date - o.date_deadline::date is null then 0 else wo.date_planned_start::date - o.date_deadline::date end, ' ', 'Days') as diff_wo_mod_date,
        # concat(case when o.date_deadline::date - p.date_deadline::date is null then 0 else o.date_deadline::date - p.date_deadline::date end, ' ', 'Days') as diff_do_mod_date,
        # concat(case when s.date_order::date - p.date_deadline::date is null then 0 else s.date_order::date - p.date_deadline::date end, ' ', 'Days') as diff_so_do_date,
        # concat(case when op.create_date::date - s.create_date::date is null then 0 else op.create_date::date - s.create_date::date end , ' ', 'Days') as diff_op_qo_date,
        # concat(case when o.date_planned_start::date - s.date_order::date is null then 0 else o.date_planned_start::date - s.date_order::date end , ' ', 'Days') as diff_so_mo_date,
        # concat(case when o.date_planned_start::date - po.date_planned::date is null then 0 else o.date_planned_start::date - po.date_planned::date end , ' ', 'Days') as diff_mo_po_date,
        # concat(case when wo.date_planned_start::date - wo.date_planned_finished::date is null then 0 else wo.date_planned_start::date - wo.date_planned_finished::date end , ' ', 'Days') as diff_wos_woe_date,
        # concat(case when wo.date_planned_start::date - o.date_deadline::date is null then 0 else wo.date_planned_start::date - o.date_deadline::date end , ' ', 'Days') as diff_wos_mod_date,
        # concat(case when po.date_planned::date - po.date_order::date is null then 0 else po.date_planned::date - po.date_order::date end , ' ', 'Days') as diff_pqo_po_date,
        # concat(case when o.date_planned_start::date - p.date_deadline::date is null then 0 else o.date_planned_start::date - p.date_deadline::date end, ' ', 'Days') as diff_mo_do_date,
        # concat(case when o.date_planned_start::date - p.installation_date::date is null then 0 else o.date_planned_start::date - p.installation_date::date end, ' ', 'Days') as diff_mo_install_date,
        
        # case when op.create_date::date - s.create_date::date is null then 0 else op.create_date::date - s.create_date::date end  as diff_op_qo_date_int,
        # case when o.date_planned_start::date - s.date_order::date is null then 0 else o.date_planned_start::date - s.date_order::date end as diff_so_mo_date_int,
        # case when o.date_planned_start::date - po.date_planned::date is null then 0 else o.date_planned_start::date - po.date_planned::date end as diff_mo_po_date_int,
        # case when wo.date_planned_start::date - wo.date_planned_finished::date is null then 0 else wo.date_planned_start::date - wo.date_planned_finished::date end  as diff_wos_woe_date_int,
        # case when wo.date_planned_finished::date - o.date_deadline::date is null then 0 else wo.date_planned_finished::date - o.date_deadline::date end as diff_wos_mod_date_int,
        # case when po.date_planned::date - po.date_order::date is null then 0 else po.date_planned::date - po.date_order::date end as diff_pqo_po_date_int,
        # case when o.date_planned_start::date - p.date_deadline::date is null then 0 else o.date_planned_start::date - p.date_deadline::date end as diff_mo_do_date_int,
        # case when o.date_planned_start::date - p.installation_date::date is null then 0 else o.date_planned_start::date - p.installation_date::date end as diff_mo_install_date_int,
        # case when s.date_order::date - po.date_planned::date is null then 0 else s.date_order::date - po.date_planned::date end  as diff_so_po_date_int,
        # case when po.date_planned::date - o.date_planned_start::date is null then 0 else po.date_planned::date - o.date_planned_start::date end as diff_po_mo_date_int,
        # case when o.date_planned_start::date - o.date_deadline::date is null then 0 else o.date_planned_start::date - o.date_deadline::date end as diff_mos_mod_date_int,
        # case when o.date_planned_start::date - wo.date_planned_start::date is null then 0 else o.date_planned_start::date - wo.date_planned_start::date end as diff_mos_wos_date_int,
        # case when wo.date_planned_start::date - o.date_deadline::date is null then 0 else wo.date_planned_start::date - o.date_deadline::date end as diff_wo_mod_date_int,
        # case when o.date_deadline::date - p.date_deadline::date is null then 0 else o.date_deadline::date - p.date_deadline::date end as diff_do_mod_date_int,
        # case when s.date_order::date - p.date_deadline::date is null then 0 else s.date_order::date - p.date_deadline::date end as diff_so_do_date_int,
        # p.name as picking_name,
        # p.id as picking_id,
        # p.state as picking_status,
        # p.date_deadline as picking_date,
        # p.installation_date as installation_date,
        # m.name as invoice_name,
        # m.id as invoice_id,
        # m.invoice_date as invoice_date,
        # o.name as mo_name,
        # o.id as mo_id,
        # o.date_planned_start as mo_start_date,
        # wo.name as wo_name,
        # wo.id as wo_id,
        # wo.date_planned_start as wo_date,
        # o.date_deadline as mo_date,
        # po.name as po_name,
        # po.id as po_id,
        # po.date_planned as po_date
        # """

        # # wo.name as wo_name,
        # # wo.date_planned_start as wo_date,

        # for field in fields.values():
        #     select_ += field

        # # from_ = """crm_lead o join sale_order s ON (o.id=s.opportunity_id)
        # from_ = """crm_lead op right join sale_order s ON (op.id=s.opportunity_id)
        # join stock_picking p ON (p.sale_id=s.id)
        # left join account_move m ON (m.invoice_origin ILIKE '%' || s.name || '%')
        # left join mrp_production o ON (o.origin ILIKE '%' || s.name || '%')
        # left join purchase_order po ON (po.origin ILIKE '%' || o.name || '%')
        # left join mrp_workorder wo ON(o.id = wo.production_id)         
        # """
        # # right join mrp_workorder wo ON(o.id = wo.production_id)
        # where_ = """op.active=TRUE AND op.type='opportunity'"""
        # # return '%s (SELECT %s FROM %s WHERE %s)' % (with_, select_, from_, where_)
        # # return '%s (SELECT %s FROM %s)' % (with_, select_, from_)

        # groupby_ = """s.id, p.id, op.name, op.create_date, s.name, s.create_date, s.date_order, p.name, p.state ,p.date_deadline, p.installation_date, 
        # m.name, m.invoice_date, o.name, o.date_planned_start, wo.name, wo.date_planned_start, o.date_deadline, po.name, po.date_planned, m.id, o.id, wo.id, po.id, op.id"""

        # orderby_ = """s.id"""

        # return '%s (SELECT %s FROM %s WHERE %s GROUP BY %s ORDER BY %s)' % (
        # with_, select_, from_, where_, groupby_, orderby_)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

    @api.model
    def get_differdays_dashboard(self, args):
        data_sets = []
        datasets = self.env['dashboard.report'].search_read([], 
                            [ 'so_name',
                             'diff_op_qo_date_int',
                             'diff_so_qo_date_int',
                             'diff_so_mo_date_int',
                             'diff_po_mo_date_int',
                             'diff_po_incom_ship_date_int',
                             'diff_mos_wos_date_int',
                             'diff_wos_woe_date_int',
                             'diff_wos_mod_date_int',
                             'diff_do_mod_date_int',
                             'diff_do_install_date_int',
                             ])
        if datasets:
            for dataset in datasets:
                data_sets.append(
                    [dataset['so_name'],[
                    dataset['diff_op_qo_date_int'],
                    dataset['diff_so_qo_date_int'],
                    dataset['diff_so_mo_date_int'],
                    dataset['diff_po_mo_date_int'], 
                    dataset['diff_po_incom_ship_date_int'],
                    dataset['diff_mos_wos_date_int'],
                    dataset['diff_wos_woe_date_int'],
                    dataset['diff_wos_mod_date_int'],
                    dataset['diff_do_mod_date_int'],
                    dataset['diff_do_install_date_int'],
                    ]]
                )
                
        return data_sets
