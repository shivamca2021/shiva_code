# -*- coding: utf-8 -*-

from odoo import api, models, fields, api, _, SUPERUSER_ID


class MailTemplate(models.TransientModel):
    _name = "template.name.wizard"

    name = fields.Char(string="Name of Template")
    mailing_id = fields.Many2one('mailing.mailing', string='Mailing')

    def save_template(self):
        for rec in self:
            if self.mailing_id.mailing_model_id and self.mailing_id.mailing_model_id.id == self.env.ref(
                    'mass_email_management.model_res_partner_groups').id:
                contact = self.env['ir.model'].search([('model', '=', 'res.partner')])
                template = self.env['mail.template'].create({
                    'name': rec.name,
                    'model_id': contact.id,
                    'body_html': rec.mailing_id.body_arch,
                })

            else:
                template = self.env['mail.template'].create({
                    'name': rec.name,
                    'model_id': rec.mailing_id.mailing_model_id.id,
                    'body_html': rec.mailing_id.body_arch,
                })
