# -*- coding: utf-8 -*-
from odoo import fields, models, api
import json


class CommissionConfig(models.Model):
    _name = 'commission.config'
    _rec_name = 'sequence'

    partner_id = fields.Many2one("res.partner", "Contact")
    commission_type = fields.Selection(
        [('gross', 'Percent of Assigned gross sale orders'), ('profit', 'Percent of Profit of Assigned Sale Orders'),
         ('amount', 'Flat Amount of Assigned Sales Orders')], string="Commission Type")
    commission_terms = fields.Selection(
        [('order', 'On Approved Order'), ('shipment', 'On Approved Shipment'), ('paid', 'Pay when Paid by Client')],
        'Terms to Pay Commission')
    amount_from = fields.Float("Target Amount (From)")
    amount_to = fields.Float("Target Amount (To)")
    commission_percentage = fields.Float("Commission Percentage")
    sequence = fields.Integer("Sequence")
    commission_amount = fields.Float("Commission Amount")
    total_sale_amount = fields.Float("contact Sales Amount")

    def name_get(self):
        result = []
        for configure in self:
            name = ''
            if configure.sequence:
                name += str(configure.sequence) + ' '
            if configure.partner_id:
                name += configure.partner_id.name
            result.append((configure.id, name))
        return result

    # @api.onchange('commission_type', 'commission_terms', 'partner_id','amount_from','amount_to')
    # def _onchange_commission_amount(self):
    #     if self.commission_type and self.commission_type and self.partner_id:
    #         if self.commission_type == 'amount' and self.commission_terms in ['order', 'shipment']:
    #             amount = 0.0
    #             orders = self.env['sale.order'].search(
    #                 [('partner_id', '=', self.partner_id.id), ('state', 'in', ['sale', 'done'])])
    #             for line in orders:
    #                 if line.amount_untaxed:
    #                     amount += line.amount_untaxed
    #             if amount >= self.amount_from and amount <= self.amount_to:
    #                 self.total_sale_amount = amount
    # elif self.commission_type == 'amount' and self.commission_terms == 'paid':


class SaleCommission(models.Model):
    _name = 'sale.commission'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one("res.partner", "Contact")
    commission_percentage = fields.Float("Commission Percentage")
    amount = fields.Float("Commission Amount")
    commission_config_id = fields.Many2one("commission.config", "Commission Configuration")
    commission_on_amount = fields.Float("Commission on Amount")

    @api.onchange('commission_config_id')
    def _onchange_commission_config_id(self):
        if self.commission_config_id and self.partner_id:
            partner_ids= self.env['res.partner'].search(['|',('id','=',self.partner_id.id), ('parent_id','=',self.partner_id.id)]).ids
            if self.commission_config_id and self.commission_config_id.commission_type == 'amount' and self.commission_config_id.commission_terms in [
                'order', 'shipment']:
                amount = 0.0

                orders = self.env['sale.order'].search(
                    [('partner_id', 'in', partner_ids), ('state', 'in', ['sale', 'done'])])
                for line in orders:
                    amount += line.amount_untaxed if line.amount_untaxed else 0
                if amount >= self.commission_config_id.amount_from and amount <= self.commission_config_id.amount_to:
                    self.amount = self.commission_config_id.commission_amount
                    self.commission_on_amount = amount
                    self.commission_percentage = 0.0
                else:
                    self.commission_percentage = 0.0
                    self.amount = 0.0
                    self.commission_on_amount = amount
            elif self.commission_config_id and self.commission_config_id.commission_type == 'amount' and self.commission_config_id.commission_terms == 'paid':
                paid_amount = 0.0
                invoices = self.env['account.move'].search(
                    [('partner_id', 'in', partner_ids), ('invoice_origin','like','S0%'), ('state', '=', 'posted'),
                     ('payment_state', 'in', ['partial', 'paid', 'in_payment'])])
                for inv in invoices:
                    invoice_payments_widget = json.loads(inv.invoice_payments_widget)
                    for amount in invoice_payments_widget.get('content'):
                        print(amount.get('amount'))
                        paid_amount += float(amount.get('amount'))
                if paid_amount >= self.commission_config_id.amount_from and paid_amount <= self.commission_config_id.amount_to:
                    self.amount = self.commission_config_id.commission_amount
                    self.commission_on_amount = paid_amount
                    self.commission_percentage = 0.0
                else:
                    self.commission_percentage = 0.0
                    self.amount = 0.0
                    self.commission_on_amount = paid_amount
            elif self.commission_config_id and self.commission_config_id.commission_type == 'gross' and self.commission_config_id.commission_terms in [
                'order', 'shipment']:
                amount = 0.0
                orders = self.env['sale.order'].search(
                    [('partner_id', 'in', partner_ids), ('state', 'in', ['sale', 'done'])])
                for line in orders:
                    amount += line.amount_untaxed if line.amount_untaxed else 0
                if amount >= self.commission_config_id.amount_from and amount <= self.commission_config_id.amount_to:
                    self.commission_percentage = self.commission_config_id.commission_percentage
                    self.amount = amount * (self.commission_config_id.commission_percentage / 100)
                    self.commission_on_amount = amount
                else:
                    self.commission_percentage = 0.0
                    self.amount = 0.0
                    self.commission_on_amount = amount
            elif self.commission_config_id and self.commission_config_id.commission_type == 'gross' and self.commission_config_id.commission_terms == 'paid':
                paid_amount = 0.0
                invoices = self.env['account.move'].search(
                    [('partner_id', 'in', partner_ids), ('invoice_origin','like','S0%'), ('state', '=', 'posted'),
                     ('payment_state', 'in', ['partial', 'paid', 'in_payment'])])
                for inv in invoices:
                    invoice_payments_widget = json.loads(inv.invoice_payments_widget)
                    for amount in invoice_payments_widget.get('content'):
                        paid_amount += float(amount.get('amount'))
                if paid_amount >= self.commission_config_id.amount_from and paid_amount <= self.commission_config_id.amount_to:
                    self.commission_percentage = self.commission_config_id.commission_percentage
                    self.amount = paid_amount * (self.commission_config_id.commission_percentage / 100)
                    self.commission_on_amount = paid_amount
                else:
                    self.commission_percentage = 0.0
                    self.amount = 0.0
                    self.commission_on_amount = paid_amount
            elif self.commission_config_id and self.commission_config_id.commission_type == 'profit' and self.commission_config_id.commission_terms in [
                'order', 'shipment']:
                amount = 0.0
                orders = self.env['sale.order'].search(
                    [('partner_id', 'in', partner_ids), ('state', 'in', ['sale', 'done'])])
                for line in orders:
                    amount += line.margin if line.margin else 0
                if amount >= self.commission_config_id.amount_from and amount <= self.commission_config_id.amount_to:
                    self.commission_percentage = self.commission_config_id.commission_percentage
                    self.amount = amount * (self.commission_config_id.commission_percentage / 100)
                    self.commission_on_amount = amount
                else:
                    self.commission_percentage = 0.0
                    self.amount = 0.0
                    self.commission_on_amount = amount
            elif self.commission_config_id and self.commission_config_id.commission_type == 'profit' and self.commission_config_id.commission_terms == 'paid':
                paid_amount = 0.0
                invoices = self.env['account.move'].search(
                    [('partner_id', 'in', partner_ids), ('invoice_origin','like','S0%'), ('state', '=', 'posted'),
                     ('payment_state', 'in', ['partial', 'paid', 'in_payment'])])
                for inv in invoices:
                    order = self.env['sale.order'].search([('name', '=', inv.invoice_origin)])
                    paid_amount += order.margin if order else 0
                # for inv in invoices:
                #     invoice_payments_widget = json.loads(inv.invoice_payments_widget)
                #     for amount in invoice_payments_widget.get('content'):
                #         paid_amount += float(amount.get('amount'))
                if paid_amount >= self.commission_config_id.amount_from and paid_amount <= self.commission_config_id.amount_to:
                    self.commission_percentage = self.commission_config_id.commission_percentage
                    self.amount = paid_amount * (self.commission_config_id.commission_percentage / 100)
                    self.commission_on_amount = paid_amount
                else:
                    self.commission_percentage = 0.0
                    self.amount = 0.0
                    self.commission_on_amount = paid_amount
        else:
            self.commission_percentage = 0.0
            self.amount = 0.0
            self.commission_on_amount = 0.0

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            configure_id = self.env['commission.config'].search(
                [('partner_id', '=', self.partner_id.id)])
            if configure_id:
                max = 0
                for conf in configure_id:
                    max = conf.id if conf.sequence > max else max
                self.commission_config_id = max
                partner_ids = self.env['res.partner'].search(
                    ['|', ('id', '=', self.partner_id.id), ('parent_id', '=', self.partner_id.id)]).ids
                if self.commission_config_id and self.commission_config_id.commission_type == 'amount' and self.commission_config_id.commission_terms in [
                    'order', 'shipment']:
                    amount = 0.0
                    orders = self.env['sale.order'].search(
                        [('partner_id', 'in', partner_ids), ('state', 'in', ['sale', 'done'])])
                    for line in orders:
                        amount += line.amount_untaxed if line.amount_untaxed else 0
                    if amount >= self.commission_config_id.amount_from and amount <= self.commission_config_id.amount_to:
                        self.amount = self.commission_config_id.commission_amount
                        self.commission_on_amount = amount
                        self.commission_percentage = 0.0
                    else:
                        self.commission_percentage = 0.0
                        self.amount = 0.0
                        self.commission_on_amount = amount
                elif self.commission_config_id and self.commission_config_id.commission_type == 'amount' and self.commission_config_id.commission_terms == 'paid':
                    paid_amount = 0.0
                    invoices = self.env['account.move'].search(
                        [('partner_id', 'in', partner_ids), ('invoice_origin','like','S0%'), ('state', '=', 'posted'),
                         ('payment_state', 'in', ['partial', 'paid', 'in_payment'])])
                    for inv in invoices:
                        invoice_payments_widget = json.loads(inv.invoice_payments_widget)
                        for amount in invoice_payments_widget.get('content'):
                            print(amount.get('amount'))
                            paid_amount += float(amount.get('amount'))
                    if paid_amount >= self.commission_config_id.amount_from and paid_amount <= self.commission_config_id.amount_to:
                        self.amount = self.commission_config_id.commission_amount
                        self.commission_on_amount = paid_amount
                        self.commission_percentage = 0.0
                    else:
                        self.commission_percentage = 0.0
                        self.amount = 0.0
                        self.commission_on_amount = paid_amount
                elif self.commission_config_id and self.commission_config_id.commission_type == 'gross' and self.commission_config_id.commission_terms in [
                    'order', 'shipment']:
                    amount = 0.0
                    orders = self.env['sale.order'].search(
                        [('partner_id', 'in', partner_ids), ('state', 'in', ['sale', 'done'])])
                    for line in orders:
                        amount += line.amount_untaxed if line.amount_untaxed else 0
                    if amount >= self.commission_config_id.amount_from and amount <= self.commission_config_id.amount_to:
                        self.commission_percentage = self.commission_config_id.commission_percentage
                        self.amount = amount * (self.commission_config_id.commission_percentage / 100)
                        self.commission_on_amount = amount
                    else:
                        self.commission_percentage = 0.0
                        self.amount = 0.0
                        self.commission_on_amount = amount
                elif self.commission_config_id and self.commission_config_id.commission_type == 'gross' and self.commission_config_id.commission_terms == 'paid':
                    paid_amount = 0.0
                    invoices = self.env['account.move'].search(
                        [('partner_id', 'in', partner_ids), ('invoice_origin','like','S0%'), ('state', '=', 'posted'),
                         ('payment_state', 'in', ['partial', 'paid',  'in_payment'])])
                    for inv in invoices:
                        invoice_payments_widget = json.loads(inv.invoice_payments_widget)
                        for amount in invoice_payments_widget.get('content'):
                            paid_amount += float(amount.get('amount'))
                    if paid_amount >= self.commission_config_id.amount_from and paid_amount <= self.commission_config_id.amount_to:
                        self.commission_percentage = self.commission_config_id.commission_percentage
                        self.amount = paid_amount * (self.commission_config_id.commission_percentage / 100)
                        self.commission_on_amount = paid_amount
                    else:
                        self.commission_percentage = 0.0
                        self.amount = 0.0
                        self.commission_on_amount = paid_amount
                elif self.commission_config_id and self.commission_config_id.commission_type == 'profit' and self.commission_config_id.commission_terms in [
                    'order', 'shipment']:
                    amount = 0.0
                    orders = self.env['sale.order'].search(
                        [('partner_id', 'in', partner_ids), ('state', 'in', ['sale', 'done'])])
                    for line in orders:
                        amount += line.margin if line.margin else 0
                    if amount >= self.commission_config_id.amount_from and amount <= self.commission_config_id.amount_to:
                        self.commission_percentage = self.commission_config_id.commission_percentage
                        self.amount = amount * (self.commission_config_id.commission_percentage / 100)
                        self.commission_on_amount = amount
                    else:
                        self.commission_percentage = 0.0
                        self.amount = 0.0
                        self.commission_on_amount = paid_amount
                elif self.commission_config_id and self.commission_config_id.commission_type == 'profit' and self.commission_config_id.commission_terms == 'paid':
                    paid_amount = 0.0
                    invoices = self.env['account.move'].search(
                        [('partner_id', 'in', partner_ids), ('invoice_origin', 'like', 'S0%'), ('state', '=', 'posted'),
                         ('payment_state', 'in', ['partial', 'paid', 'in_payment'])])
                    for inv in invoices:
                        order=self.env['sale.order'].search([('name', '=', inv.invoice_origin)])
                        paid_amount += order.margin if order else 0
                    # for inv in invoices:
                    #     invoice_payments_widget = json.loads(inv.invoice_payments_widget)
                    #     for amount in invoice_payments_widget.get('content'):
                    #         paid_amount += float(amount.get('amount'))
                    if paid_amount >= self.commission_config_id.amount_from and paid_amount <= self.commission_config_id.amount_to:
                        self.commission_percentage = self.commission_config_id.commission_percentage
                        self.amount = paid_amount * (self.commission_config_id.commission_percentage / 100)
                        self.commission_on_amount = paid_amount
                    else:
                        self.commission_percentage = 0.0
                        self.amount = 0.0
                        self.commission_on_amount = paid_amount

            else:
                self.commission_config_id = False
                self.commission_percentage = 0.0
                self.amount = 0.0
                self.commission_on_amount = 0.0
        else:
            self.commission_config_id = False
            self.commission_percentage = 0.0
            self.amount = 0.0
            self.commission_on_amount = 0.0