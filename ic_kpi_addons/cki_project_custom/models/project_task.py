from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
from datetime import datetime, timedelta


class ProjectTask(models.Model):
    _inherit = "project.task"
    _description = 'Project Task'
    
    @api.model
    def _default_end_date(self):
        defaults = self.default_get(['project_id', 'stage_id','stage_start_date'])
        if 'project_id' in defaults.keys() and defaults['stage_id']:
            stage_obj = self.env['project.task.type'].search([
                    ('project_ids','in',[defaults['project_id']]),('id','=',defaults['stage_id'])])
            if stage_obj.buffer_days > 0:
                buffer_days = stage_obj.buffer_days
                add_days = buffer_days - 1
                for x in range(buffer_days):
                    index = x 
                    Enddate = defaults['stage_start_date'] + timedelta(days=index)
                    if Enddate.weekday() in [5,6]:
                        add_days += 1
                    if buffer_days == x + 1:
                        Enddate = defaults['stage_start_date'] + timedelta(days=add_days)
                        if Enddate.weekday() in [5,6]:
                            add_days += 1
                Enddate = defaults['stage_start_date'] + timedelta(days=add_days)
                return Enddate
        return datetime.now()
    
    @api.depends('stage_end_date_calender')
    def _compute_stage_end_date_calender(self):
        for task in self:
            if task.stage_end_date:
                new_date = (datetime.strptime(str(task.stage_end_date), '%Y-%m-%d') + date_utils.relativedelta(days =+ 1))
                task.stage_end_date_calender = new_date
            else:
                task.stage_end_date_calender = False
                
    def _get_default_stage_id(self):
        """ Gives default stage_id """
        project_id = self.env.context.get('default_project_id')
        if not project_id:
            return False
        return self.stage_find(project_id, [('fold', '=', False), ('is_closed', '=', False)])
    
    capacity = fields.Float(string='Demand', tracking=True,help="Demand Value")
    uom_id = fields.Many2one(related='stage_id.uom_id', related_sudo=False, string="Unit of Measure")
    per_uom_id = fields.Many2one(related='stage_id.per_uom_id', related_sudo=False, string="Per Unit of Measure")
    stage_start_date  = fields.Date('Stage Start Date', tracking=True, help="Stage Start Date", default=fields.Datetime.now, copy=True)
    stage_end_date_calender = fields.Date( compute=_compute_stage_end_date_calender, copy=True)
    stage_end_date  = fields.Date('Stage End Date', tracking=True, help="Stage End Date",default=_default_end_date, copy=True)
    is_capacity_exceed = fields.Boolean(string='Capacity Exceed?',help="Do you want to override Stage Capacity?" , tracking=True)
    capacity_tooltip = fields.Char(default="**Do you want to override Stage Capacity?", readonly=True)
    allday = fields.Boolean('All Day', default=True, copy=True)
    stage_id = fields.Many2one('project.task.type', string='Stage', compute='_compute_stage_id',
        store=True, readonly=False, ondelete='restrict', tracking=True, index=True,
        default=_get_default_stage_id, group_expand='_read_group_stage_ids',
        domain="[('project_ids', '=', project_id)]", copy=True)
    
    @api.constrains('stage_start_date')
    def _validate_stage_start_date(self):
        if not self.stage_start_date and self.stage_end_date:
            raise ValidationError(_("Stage Start Date is Required."))
        if self.stage_start_date and self.stage_end_date:
            if self.stage_start_date > self.stage_end_date:
                raise ValidationError(_("Stage Start Date must be less than or equal to Stage End Date."))
        
    @api.constrains('stage_end_date')
    def _validate_stage_end_date(self):
        if self.stage_end_date:
            if self.stage_start_date > self.stage_end_date:
                raise ValidationError(_("Stage Start Date must be greater than or equal to Stage End Date."))
            
    @api.constrains('capacity')
    def _validate_capacity(self):
        all_sm_stage_capacity = sum(self.project_id.task_ids.filtered(lambda x: x.stage_id == self.stage_id).mapped('capacity'))
        stage_capacity = self.stage_id.capacity
        if stage_capacity > 0:
            if all_sm_stage_capacity > stage_capacity and not self.is_capacity_exceed:
                raise ValidationError(_("Task Capacity Exceed Stage Capacity!."))

            
    def write(self, vals):
        if vals.get('stage_id', False):
            if vals.get('stage_id') != self.stage_id:
                vals.update({'stage_start_date':False,'stage_end_date':False,'capacity':0.0,'is_capacity_exceed':False})
        return super(ProjectTask, self).write(vals)
    
    @api.model
    def get_stage_capacity(self, args):
        try:
            stage = self.env['project.task.type'].browse(int(args['stage_id']))
        except:
            stage = self.env['project.task.type']
        stage_capacity = stage.capacity if stage else 0.0
        final_capacity = _("%s %s %s") % (stage_capacity,stage.uom_id.name or '',stage.per_uom_id.name or '')
        return [final_capacity]
