from odoo import fields, models, api, _


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    stage_start_date = fields.Date(related='task_id.stage_start_date', string='Stage Start Date', tracking=True,
                                   help="Stage Start Date",
                                   store=True)
    stage_end_date = fields.Date(related='task_id.stage_end_date', string='Stage End Date', tracking=True,
                                 help="Stage End Date", store=True)

    date_deadline = fields.Date(related='task_id.date_deadline', string='Deadline', tracking=True,
                                store=True)
    planned_hours = fields.Float(related='task_id.planned_hours', string='Initially Planned Hours', tracking=True,
                                 store=True)
    stage_id = fields.Many2one(related='task_id.stage_id', string='Status', tracking=True,
                                 store=True)
    task_number = fields.Char(related='task_id.task_number', string='Task Number', tracking=True,
                                  store=True)

class ProjectTask(models.Model):
    _inherit = "project.task"

    task_number = fields.Char("Task Number", readonly=True, index=True, default=lambda self: _(''))

    @api.model
    def create(self, vals):
        if vals.get('task_number', _('')) == _(''):
            vals['task_number'] = self.env['ir.sequence'].next_by_code('project.task') or _('')
        result = super(ProjectTask, self).create(vals)
        return result
