from odoo import fields,models,api,_
from lxml import etree

class Partner(models.Model):
    _inherit = 'res.partner'

    def action_duplicate_contacts(self):
        self._cr.execute("""
                    select email from res_partner where active=True and email is not null group by email having count(*)>1
                    """)
        distinct_data = self._cr.fetchall()
        distinct_id = [item for t in distinct_data for item in t]
        records = []
        records.extend(self.sudo().search([('email', 'in', distinct_id)]).ids)
        domain = [('id', 'in', records)]
        action = self.env["ir.actions.actions"]._for_xml_id("ickpi_filter.action_duplicates_contacts")
        action['domain'] = domain
        if self.env.context.get('duplicate_read'):
            return domain
        return action

