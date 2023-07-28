from odoo import api, fields, models, _

class MrpProductWizard(models.TransientModel):
    _name = 'project.task.wizard'
    
    confirm = fields.Char()
    task_id = fields.Many2one('project.task', string='Task')
   
    def action_done(self):
        return True
    
    def action_cancel(self):
        return False