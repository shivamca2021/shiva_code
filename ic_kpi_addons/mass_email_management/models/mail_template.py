# -*- coding: utf-8 -*-

from odoo import api, models, fields, api, _, SUPERUSER_ID


class MailTemplate(models.Model):
    _inherit = "mail.template"

    body_html_2 = fields.Html(string="Html New")