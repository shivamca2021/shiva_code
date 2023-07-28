from odoo import models, fields, api, _


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('freight_charge')
    def _amount_freigt(self):
        self.amount_total = self.amount_total + self.freight_charge

    est_ship_date = fields.Datetime('Estimated Shipping Date')
    shipper = fields.Char('Shipper')
    prepaid = fields.Char('Prepaid')
    freight_charge = fields.Float('Freight Charge')
    qms_notes = fields.Text('QMS REQUIREMENTS',
                        default='FALCON RIGWERX QMS REQUIREMENTS\n'
                                'IF APPLICABLE EVERY VENDOR MUST SUPPLY THE FOLLOWING:\n'
                                'MTR REPORTS, CERTIFICATES OF CONFORMANCE, TEST REPORTS, DATA SHEETS, NDE REPORTS, PERSONNEL QUALIFICATIONS AND/OR CERTIFICATIONS, CERTIFICATES OF CALIBRATION, OR ANY OTHER DOCUMENTATION '
                                'SPECIFICALLY NOTED ON THE PURCHASE ORDER.')
