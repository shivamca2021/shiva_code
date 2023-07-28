from odoo import fields, models, api

class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    def _get_name(self):
        name = super(PartnerInherit, self)._get_name()
        if self._context.get('show_phone') and self.phone:
            name = "%s\n%s" % (name, self.phone)
        return name