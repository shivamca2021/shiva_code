from odoo import api, fields, models, _

class PerUom(models.Model):
    _name = "per.uom"
    _description = 'per uom'
    
    name = fields.Char(string='Name')
    

class ProjectStage(models.Model):
    _inherit = "project.task.type"
    _description = 'Project Task Type'
    
    capacity = fields.Float(string='Capacity')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    per_uom_id = fields.Many2one('per.uom', string='Per Unit of Measure')


class ProjectProject(models.Model):
    _inherit = "project.project"
    _description = 'Project'

    def custom_copy(self):
        for record in self:
            record.sudo().copy()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }