# -*- coding: utf-8 -*-

from odoo import api, models, fields, api, _, SUPERUSER_ID
from odoo.osv import expression #1st feb added
import random

MASS_MAILING_BUSINESS_MODELS = [
    'crm.lead',
    'event.registration',
    'hr.applicant',
    'res.partner',
    'event.track',
    'sale.order',
    'mailing.list',
    'mailing.contact',
    'res.partner.groups'
]


class MassMailing(models.Model):
    _inherit = "mailing.mailing"

    template_id = fields.Many2one('mail.template', string='Email Template', index=True, domain="[('model_id', '=', mailing_model_id)]")
    mailing_model_id = fields.Many2one(
        'ir.model', string='Recipients Model', ondelete='cascade', required=True,
        domain=[('model', 'in', MASS_MAILING_BUSINESS_MODELS)],
        default=lambda self: self.env.ref('mass_mailing.model_mailing_list').id)
    contact_group_ids = fields.Many2many('res.partner.groups', 'mailing_mailing_res_partner_groups_rel', string='Contact Groups')

    @api.depends('mailing_model_id')
    def _compute_model(self):
        for record in self:
            if record.mailing_model_name == 'mailing.list':
                record.mailing_model_real = 'mailing.contact'
            elif record.mailing_model_name == 'res.partner.groups':
                record.mailing_model_real = 'res.partner'
            else:
                record.mailing_model_real = record.mailing_model_name

    @api.onchange('mailing_model_id')
    def _onchange_mailing_model_id(self):
        res = {}
        if self.mailing_model_id and self.mailing_model_id.id == self.env.ref('mass_email_management.model_res_partner_groups').id:
            template_ids = []
            for template_id in self.env['mail.template'].search([('model', '=', 'res.partner')]):
                template_ids.append(template_id.id)
            res['domain'] = {'template_id': [('id', 'in', template_ids)]}
        return res
    
    def _get_recipients(self):
        mailing_domain = self._parse_mailing_domain()
        ids = []
        if self.mailing_model_id.model == 'res.partner.groups':
            for rec in self.contact_group_ids:
                partner_ids = rec.partner_ids.filtered(lambda x:not x.opt_out)
                for record in partner_ids:
                    ids.append(record.id)
            res_ids = ids
        else:
            res_ids = self.env[self.mailing_model_real].search(mailing_domain).ids

        # randomly choose a fragment
        if self.contact_ab_pc < 100:
            contact_nbr = self.env[self.mailing_model_real].search_count(mailing_domain)
            topick = int(contact_nbr / 100.0 * self.contact_ab_pc)
            if self.campaign_id and self.unique_ab_testing:
                already_mailed = self.campaign_id._get_mailing_recipients()[self.campaign_id.id]
            else:
                already_mailed = set([])
            remaining = set(res_ids).difference(already_mailed)
            if topick > len(remaining):
                topick = len(remaining)
            res_ids = random.sample(remaining, topick)
        return res_ids

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self.body_html = self.template_id.body_html
            self.body_arch = self.template_id.body_html

    def action_save_template(self):

            return {
                'name': 'Template Name',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'template.name.wizard',
                'view_id': False,
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context': {'default_mailing_id': self.id}
            }

    #1st feb updated start
    def _get_default_mailing_domain(self):
        res = super(MassMailing, self)._get_default_mailing_domain()
        if self.mailing_model_name == 'res.partner':
            res = expression.AND([[("opt_out","=",False)], res])
        if self.mailing_model_name == 'res.partner.groups':
            res = [("opt_out","=",False),('partner_groups_ids', 'in', self.contact_group_ids.ids)]
        return res

    @api.depends('mailing_model_id', 'contact_list_ids', 'contact_group_ids', 'mailing_type')
    def _compute_mailing_domain(self):
        for mailing in self:
            if not mailing.mailing_model_id:
                mailing.mailing_domain = ''
            else:
                mailing.mailing_domain = repr(mailing._get_default_mailing_domain())
    #1st feb updated end
