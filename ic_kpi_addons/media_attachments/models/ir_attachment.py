
from odoo import api, fields, models, tools, _


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'


    def generate_access_token(self):
        tokens = []
        for attachment in self:
            if attachment.access_token:
                tokens.append(attachment.access_token)
                continue
            access_token = self._generate_access_token()
            existing = self.sudo().search([('name', '=', attachment.name), ('public', '=', True)], limit=1)
            if not existing:
                attachment.write({'access_token': access_token, 'public': True})
            else:
                attachment.write({'access_token': access_token})
            tokens.append(access_token)
        return tokens
