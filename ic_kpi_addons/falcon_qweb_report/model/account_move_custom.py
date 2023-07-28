from odoo import models, fields, api, _


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    work_description = fields.Char('DESCRIPTION OF WORK')
    terms_note = fields.Char('Terms')
