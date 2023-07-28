from odoo import models, fields, api, _



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'




class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order'
