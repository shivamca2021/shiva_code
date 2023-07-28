
from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.render.mixin"

    def _replace_local_links(self, html, base_url=None):
        html = super()._replace_local_links(html, base_url=base_url)
        print("-----------------------------------",html)
        html_debranded = self.env["mail.template"]._debrand_body(html)
        return html_debranded
