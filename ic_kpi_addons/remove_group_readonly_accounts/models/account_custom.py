from odoo import models, fields, api, _


class AccountInherit(models.Model):
    _inherit = 'account.account'

    group_id = fields.Many2one('account.group', compute='_compute_account_group', store=True, readonly=False)

