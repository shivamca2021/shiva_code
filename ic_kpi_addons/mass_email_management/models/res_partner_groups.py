# -*- coding: utf-8 -*-

from odoo import api, models, fields, api, _, SUPERUSER_ID
from lxml import etree

class ResPartnerGroups(models.Model):
    _name = "res.partner.groups"
    _description = "To Manage Groups of Partners"

    name = fields.Char('Name Of Group')
    partner_ids = fields.Many2many('res.partner', column1='group_id', column2='partner_id', string='Contacts')
    #1st feb updated start
    count_of_partner = fields.Integer(string="Count Of Partners", compute='_get_count_of_partners', help="It shows the count of partners")
    contact_to_show = fields.Integer(string="Not Optout Count Of Partner", compute='_get_count_of_partners', help="It shows the count of partners that is not opt_out")

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(ResPartnerGroups, self).fields_view_get(
    #         view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #     for node in doc.xpath("//field[@name='partner_ids']"):
    #         print(node)
    #         self._cr.execute("""
    #                             SELECT DISTINCT on (email) id FROM res_partner where email is not null order by email,write_date DESC
    #                             """)
    #         distinct_data = self._cr.fetchall()
    #         distinct_id = [item for t in distinct_data for item in t]
    #         self._cr.execute("""
    #                                             SELECT id FROM res_partner where email is null;
    #                                             """)
    #         email_not_set_data = self._cr.fetchall()
    #         email_not_set_id = [item for t in email_not_set_data for item in t]
    #         distinct_id.extend(email_not_set_id)
    #         node.set(
    #             'domain', "[('id','in',%s)]" % distinct_id)
    #     res['arch'] = etree.tostring(doc)
    #     return res

    @api.depends('partner_ids')
    def _get_count_of_partners(self):
        for group_partner in self:
            group_partner.count_of_partner = 0
            group_partner.contact_to_show = 0
            partner_ids = group_partner.partner_ids 
            if partner_ids:
                group_partner.count_of_partner = len(partner_ids)
                group_partner.contact_to_show = len(partner_ids.filtered(lambda x: not x.opt_out))

    @api.model
    def create(self, vals):
        res = super(ResPartnerGroups, self).create(vals)
        for partner in res.partner_ids:
            partner.sudo().write({'partner_groups_ids': [(4, res.id)]})
        return res

    def write(self, vals):
        res = super(ResPartnerGroups, self).write(vals)
        if 'partner_ids' in vals:
            for partner in self.partner_ids:
                partner.sudo().write({'partner_groups_ids' :[(4, self.id)]})
        return res

    def name_get(self):
        return [(group.id, "%s (%s)" % (group.name, group.contact_to_show)) for group in self]

class ResPartner(models.Model):
    _inherit = "res.partner"

    opt_out = fields.Boolean(string="Opt Out", default=False, tracking=True, help="It shows partner is opt out or not")
    partner_groups_ids = fields.Many2many(
        'res.partner.groups', 'res_partner_groups_list_rel',
        'partner_id', 'group_id', string='Partner Group Lists')
    # 1st feb updated end
