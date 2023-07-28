from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging
import threading
import psycopg2
import base64
from odoo import api, fields, models, modules, tools, _
from odoo.exceptions import AccessDenied, UserError
_logger = logging.getLogger(__name__)

class ResUser(models.Model):
  _inherit = 'res.users'

  notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in Prism')],
        'Notification', required=True, default='email',
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email address\n"
             "- Handle in Prism: notifications appear in your Prism Inbox")

  odoobot_state = fields.Selection(
        [
            ('not_initialized', 'Not initialized'),
            ('onboarding_emoji', 'Onboarding emoji'),
            ('onboarding_attachement', 'Onboarding attachement'),
            ('onboarding_command', 'Onboarding command'),
            ('onboarding_ping', 'Onboarding ping'),
            ('idle', 'Idle'),
            ('disabled', 'Disabled'),
        ], string="Bot Status", readonly=True, required=False)

class OdooDebrand(models.Model):
    _inherit = 'website'

    @api.depends('favicon')
    def get_favicon(self):
        self.favicon_url = \
            'data:image/png;base64,' + str(self.favicon.decode('UTF-8'))
        # python 3.x has sequence of bytes object,
        #  so we should decode it, else we get data starting with 'b'

    @api.depends('company_logo')
    def get_company_logo(self):
        self.company_logo_url = \
            ('data:image/png;base64,' +
             str(self.company_logo.decode('UTF-8')))

    company_logo = fields.Binary("Logo", attachment=True,
                                 help="This field holds"
                                      " the image used "
                                      "for the Company Logo")
    company_name = fields.Char("Company Name", help="Branding Name")
    company_website = fields.Char("Company URL")
    favicon_url = fields.Char("Url", compute='get_favicon')
    company_logo_url = fields.Char("Url", compute='get_company_logo')


class WebsiteConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    company_logo = fields.Binary(related='website_id.company_logo',
                                 string="Company Logo",
                                 help="This field holds the image"
                                      " used for the Company Logo",
                                 readonly=False)
    company_name = fields.Char(related='website_id.company_name',
                               string="Company Name",
                               readonly=False)
    company_website = fields.Char(related='website_id.company_website',
                                  readonly=False)

    # Sample Error Dialogue
    def error(self):
        raise ValueError

    # Sample Warning Dialogue
    def warning(self):
        raise Warning(_("This is a Warning"))


class Module(models.Model):
    _inherit = "ir.module.module"
    _rec_name = "shortdesc"
    _description = "Module"
    _order = 'application desc,sequence,name'



    def _button_immediate_function(self, function):
        if getattr(threading.currentThread(), 'testing', False):
            raise RuntimeError(
                "Module operations inside tests are not transactional and thus forbidden.\n"
                "If you really need to perform module operations to test a specific behavior, it "
                "is best to write it as a standalone script, and ask the runbot/metastorm team "
                "for help."
            )
        try:
            # This is done because the installation/uninstallation/upgrade can modify a currently
            # running cron job and prevent it from finishing, and since the ir_cron table is locked
            # during execution, the lock won't be released until timeout.
            self._cr.execute("SELECT * FROM ir_cron FOR UPDATE NOWAIT")
        except psycopg2.OperationalError:
            raise UserError(_("Prism is currently processing a scheduled action.\n"
                              "Module operations are not possible at this time, "
                              "please try again later or contact your system administrator."))
        function(self)

        self._cr.commit()
        api.Environment.reset()
        modules.registry.Registry.new(self._cr.dbname, update_module=True)

        self._cr.commit()
        env = api.Environment(self._cr, self._uid, self._context)
        # pylint: disable=next-method-called
        config = env['ir.module.module'].next() or {}
        if config.get('type') not in ('ir.actions.act_window_close',):
            return config

        # reload the client; open the first available root menu
        menu = env['ir.ui.menu'].search([('parent_id', '=', False)])[:1]
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {'menu_id': menu.id},
        }


class Channel(models.Model):
    _inherit = 'mail.channel'

    def _get_default_image(self):
        image_path = modules.get_module_resource('prism_odoo_rebranding', 'static/src/img', 'groupdefault.png')
        return base64.b64encode(open(image_path, 'rb').read())

    image_128 = fields.Image("Image", max_width=128, max_height=128, default=_get_default_image)

    @api.model
    def init_odoobot(self):
        if self.env.user.odoobot_state in [False, 'not_initialized']:
            odoobot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
            channel_info = self.channel_get([odoobot_id])
            channel = self.browse(channel_info['id'])
            message = _(
                "Hello,<br/>Prism's chat helps employees collaborate efficiently. I'm here to help you discover its features.<br/><b>Try to send me an emoji</b> <span class=\"o_odoobot_command\">:)</span>")
            channel.sudo().message_post(body=message, author_id=odoobot_id, message_type="comment",
                                        subtype_xmlid="mail.mt_comment")
            self.env.user.odoobot_state = 'onboarding_emoji'
            return channel
