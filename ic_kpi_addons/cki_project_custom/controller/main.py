import logging
from odoo.http import request
from odoo import http, _, exceptions


_logger = logging.getLogger(__name__)

class ArchiveModel(http.Controller):

    @http.route(['/cki/project/archive'], type='json', auth='public', website=True)
    def action_check_archive_user_model(self, **post):
        values = {}
        if post.get('uid'):
            user_id = request.env['res.users'].sudo().browse(int(post['uid']))
            if user_id.has_group('project.group_project_user') and not user_id.has_group('project.group_project_manager') and not user_id.has_group('cki_project_custom.group_project_manager_cki'):
                values.update({'access': False})
            else:
                values.update({'access': True})
        return values
