from odoo import models, fields, api, _


class SaleOrderEstimationInherit(models.Model):
    _inherit = 'sale.order'

    @api.depends('amount_total')
    def _compute_estimation_amount(self):

        for rec in self:
            rec.deposit_amount = rec.balance_amount = rec.total_estimate_amount = 0
            if rec.amount_total:
                rec.deposit_amount = (rec.amount_total*(50/100))
                rec.balance_amount = (rec.amount_total - rec.deposit_amount)
                rec.total_estimate_amount = rec.balance_amount

    work_description = fields.Char('DESCRIPTION OF WORK')
    # prepaid = fields.Char('Prepaid')
    deposit_amount = fields.Float('Deposit Amount', compute='_compute_estimation_amount',)
    balance_amount = fields.Float('Balance Amount')
    total_estimate_amount = fields.Float('Estimated Amount')
    estimation_note = fields.Char('Terms and Conditions',
                                  default='NOTE: THIS ESTIMATE IS NOT A CONTRACT OR BILL.'
                                          ' IT IS OUR BEST GUESS AT THE TOTAL PRICE TO COMPLETE THE  WORK STATED ABOVE, BASED ON OUR INITIAL INSPECTION. '
                                          'IF PRICES CHANGE OR ADDITIONAL PARTS ARE REQUIRED,WE WILL EMAIL YOU A CHANGE ORDER REQUEST FOR YOUR APPROVAL BEFORE PROCEEDING ANY WORK.')

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrderEstimationInherit, self)._prepare_invoice()
        invoice_vals['work_description'] = self.work_description
        invoice_vals['terms_note'] = self.estimation_note
        return invoice_vals
