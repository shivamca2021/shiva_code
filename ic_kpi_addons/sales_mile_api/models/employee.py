# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

log = logging.getLogger(__name__)


class HrEmpolyee(models.Model):
    _inherit = "hr.employee"

    def _set_username(self):
        for rec in self:
            if rec.work_email:
                username = str(rec.work_email).split('@')[0]
                rec.username = username
            else:
                rec.username = False

    user_name = fields.Char(stirng='Username', store=True)
    password = fields.Char(stirng='Password')

    _sql_constraints = [
        ('name_user_name', 'unique (user_name)', "UserName already exists !"),
    ]

    def verify_credentials(self, username, password):
        emp = self.sudo().search([('user_name', '=', username), ('password', '=', password)], limit=1)
        if emp:
            return {
                'name': emp.name,
                'user_id': emp.user_id.id
            }
        return False
