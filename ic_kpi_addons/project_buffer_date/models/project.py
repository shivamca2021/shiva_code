from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.tools import date_utils
from odoo.exceptions import ValidationError, UserError



class ProjectProject(models.Model):
    _inherit = "project.project"
    _description = 'Project'
    
    buffer_date_calculate = fields.Boolean(string='Calculate with buffer date',help="Do you want to Calculate with buffer date?" )
    template_project = fields.Boolean('Template Project')

    @api.model
    def create(self, vals):
        if vals.get('template_project'):
            existing = self.sudo().search([('template_project', '=', True)],limit=1)
            if existing:
                raise ValidationError(_("Template Project is Already selected in %s.") % (existing.name))
            vals.update({'color':9})
        project = super(ProjectProject, self).create(vals)
        return project

    def write(self, vals):
        for record in self:
            if vals.get('template_project'):
                existing = self.sudo().search([('template_project', '=', True),('id','!=',record.id)], limit=1)
                if existing:
                    raise ValidationError(_("Template Project is Already selected in %s.") % (existing.name))
                vals.update({'color': 9})
            if vals.get('template_project') == False:
                vals.update({'color': False})
        return super(ProjectProject, self).write(vals)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not self.template_project:
            raise UserError(_('You cannot duplicate Non Template Project! '))
        default['template_project'] = False
        default['color'] = False
        return super(ProjectProject, self).copy(default)

class ProjectTask(models.Model):
    _inherit = "project.task"
    _description = 'Project Task'
    
    @api.depends('stage_start_date', 'stage_end_date')
    def _compute_updated_stages(self):
        for task in self:
            buffer_stages = []
            final_lst = []
            stage_objs = self.env['project.task.type'].search([
                ('project_ids','in',[task.project_id.id])], order="sequence asc").ids
            line_stages = task.buffer_stage_id.mapped('stage_id').ids
            stage_objs.sort()
            line_stages.sort()
            if(stage_objs==line_stages):
                pass
            else:
                if len(line_stages) > len(stage_objs):
                    final_lst = list(set(line_stages) - set(stage_objs))
                else:
                    final_lst = list(set(stage_objs) - set(line_stages))
            if final_lst:
                if task.stage_end_date:
                    sch_list = task.compute_stages_scheduled(task.stage_end_date, task)
                    for index in sch_list:
                        task.buffer_stage_id = [[5,]]
                        for key, value in index.items():
                            stage_obj = self.env['project.task.type'].browse(int(key))
                            task_line = {'name':task.name + ' ('+stage_obj.name+')',
                                              'stage_task_id':task.id,
                                              'stage_id':stage_obj.id,
                                              'user_id':task.user_id.id,
                                              'stage_start_date':value[0],
                                              'stage_end_date':value[1],
                                              'project_id':task.project_id.id,
                                              'sequence':stage_obj.sequence}
                            buffer_stages.append([0,0,task_line])
            task.buffer_stage_id = buffer_stages
            task.show_new_stage = True
            
    @api.depends('stage_start_date', 'stage_end_date')
    def _compute_stages_start_date(self):
        for record in self:
            record.is_start_date_exceed = ''
            if record.stage_id:
                current_stage = record.buffer_stage_id.filtered(lambda x: x.stage_id == record.stage_id)
                if current_stage:
                    if (record.stage_start_date and current_stage[0].start_date and record.stage_start_date > current_stage[0].start_date) or (record.stage_end_date and current_stage[0].end_date and record.stage_end_date > current_stage[0].end_date):
                        record.is_start_date_exceed = 'exceed_class'
            
    
#     buffer_stage_id = fields.One2many('project.task.stage', 'stage_task_id', string='Task')
    buffer_stage_id = fields.Many2many("project.task.stage", string="Stage Name",
                                          domain="[('stage_task_id' , '=' , id)]", ondelete='cascade')
    show_new_stage = fields.Boolean(compute='_compute_updated_stages')
    is_start_date_exceed = fields.Char(compute='_compute_stages_start_date')
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    
    
    @api.model
    def create(self, data):
        rec = super(ProjectTask, self).create(data)
        stages = [i for i in self.env['project.task.type'].search([('project_ids','in',[rec.project_id.id])],
                                                                  order='sequence asc')]
        task_schedule, start_date, end_date, previous_task, stage_schedule = [], None, None, None, None
        pre_stg_obj = self.env['project.task.stage']
        for stage in stages:
            if self:
                pre_stg_obj = self.env['project.task.stage'].search([('stage_task_id','=',self.id),('stage_id','=',stage.id)])
            if not (start_date and end_date):
                import datetime
                start_date = datetime.date.today()
                if start_date.weekday() == 5:
                    start_date += timedelta(days=2)
                elif start_date.weekday() == 6:
                    start_date += timedelta(days=1)
                end_date = start_date + timedelta(days=stage.buffer_days)
                total_days = [start_date + timedelta(x) for x in range((end_date - start_date).days + 1)]
                off_days = sum(1 for day in total_days if day.weekday() >= 5)
                if off_days:
                    end_date = start_date + timedelta(days=stage.buffer_days + off_days + 1)
                if end_date.weekday() == 5:
                    end_date += timedelta(days=2)
                elif end_date.weekday() == 6:
                    end_date += timedelta(days=1)
            else:
                start_date = stage_schedule.end_date + timedelta(days=1)
                if start_date.weekday() == 5:
                    start_date += timedelta(days=2)
                elif start_date.weekday() == 6:
                    start_date += timedelta(days=1)
                end_date = start_date + timedelta(days=stage.buffer_days)
                total_days = [start_date + timedelta(x) for x in range((end_date - start_date).days)]
                off_days = sum(1 for day in total_days if day.weekday() >= 5)
                if off_days:
                    end_date = start_date + timedelta(days=stage.buffer_days + off_days)
                if end_date.weekday() == 5:
                    end_date += timedelta(days=2)
                elif end_date.weekday() == 6:
                    end_date += timedelta(days=1)
#             stage_schedule = self.env['project.task.schedule'].create({'stage_id': stage.id,
#                                                                        'task_id': rec.id,
#                                                                        'start_date': start_date,
#                                                                        'end_date': end_date})
            stage_schedule = self.env['project.task.stage'].create({'name':rec.name + ' ('+stage.name+')',
                                                'stage_task_id':rec.id,
                                                'stage_id':stage.id,
                                                'user_id':rec.user_id.id,
                                                'start_date':rec.stage_start_date,
                                                'end_date':rec.stage_end_date,
                                                'project_id':rec.project_id.id,
                                                'sequence':stage.sequence,
                                                'hide_on_calender':pre_stg_obj.hide_on_calender})
            task_schedule.append(stage_schedule.id)
        rec.buffer_stage_id = task_schedule
        return rec

    @api.onchange("buffer_stage_id")
    def onchange_task_type(self):
        last_stage = None
        for stage in self.buffer_stage_id:
            if not stage.start_date:
                stage.start_date = self.create_date.date()
            if stage.start_date.weekday() == 5:
                stage.start_date += timedelta(days=2)
            elif stage.start_date.weekday() == 6:
                stage.start_date += timedelta(days=1)
            stage.end_date = stage.start_date + timedelta(days=stage.stage_id.buffer_days)
            if stage.end_date.weekday() == 5:
                stage.end_date += timedelta(days=2)
            elif stage.end_date.weekday() == 6:
                stage.end_date += timedelta(days=1)
            if last_stage:
                stage.start_date = last_stage.end_date + timedelta(days=1)
                if stage.start_date.weekday() == 5:
                    stage.start_date += timedelta(days=2)
                elif stage.start_date.weekday() == 6:
                    stage.start_date += timedelta(days=1)
                stage.end_date = stage.start_date + timedelta(days=stage.stage_id.buffer_days)
                if stage.end_date.weekday() == 5:
                    stage.end_date += timedelta(days=2)
                elif stage.end_date.weekday() == 6:
                    stage.end_date += timedelta(days=1)
                last_stage = stage
            else:
                last_stage = stage

    @api.onchange('stage_start_date')
    def _onchange_stage_start_date(self):
        if self.stage_start_date:
            self.date_start = self.stage_start_date
        if self.stage_end_date:
            self.date_end = self.stage_end_date
            
    @api.onchange('stage_end_date')
    def _onchange_stage_end_date(self):
        if self.stage_start_date:
            self.date_start = self.stage_start_date
        if self.stage_end_date:
            self.date_end = self.stage_end_date
    
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        default['is_capacity_exceed'] = True
        if self.stage_start_date:
            default['stage_start_date'] = self.stage_start_date
        if self.stage_end_date:
            default['stage_end_date'] = self.stage_end_date
        return super(ProjectTask, self).copy(default)
    
    
    
#     def compute_stages_scheduled(self, end_date, task):
#         """ To compute scheduled dates for stages
#         :param task: respective task
#         :param end_date: the end date of task for stage sequence 1
#         :return: Iterable of list {stage_id: [start date, End date]}
#         """
#         final_lst = []
#         start_date = datetime.strptime(str(end_date), '%Y-%m-%d') if end_date else ''
#         stage_objs = self.env['project.task.type'].search([('project_ids','in',[task.project_id.id]),('sequence','>=',task.stage_id.sequence)], order="sequence asc")
#         
#         if stage_objs:
#             lst_buffer_days = stage_objs.mapped('buffer_days')
#             for count, stage_obj in enumerate(stage_objs):
#                 days = 0
#                 if count < (len(stage_objs) - 1 ):
#                     count += 1
#                     bf_days = lst_buffer_days[count]
#                     if bf_days > 0:
#                         days = 1
#                 stage_lst = []
# #                 start_date = start_date + timedelta(days=days)
#                 if task.stage_id == stage_obj:
#                     stage_lst.append(task.stage_start_date)
#                     stage_lst.append(task.stage_end_date)
#                     stage_dict = {stage_obj.id:stage_lst}
#                     final_lst.append(stage_dict)
#                     Enddate = task.stage_end_date
#                 elif start_date and task.stage_id:
#                     stage_lst.append(start_date)
#                     if stage_obj.buffer_days:
#                         buffer_days = stage_obj.buffer_days
#                         add_days = buffer_days - 1
#                         for x in range(buffer_days):
#                             index = x 
#                             Enddate = start_date + timedelta(days=index)
#                             if Enddate.weekday() in [5,6]:
#                                 add_days += 1
#                             if buffer_days == x + 1:
#                                 Enddate = start_date + timedelta(days=add_days)
#                                 if Enddate.weekday() in [5,6]:
#                                     add_days += 1
#                         Enddate = start_date + timedelta(days=add_days)
#                         stage_lst.append(Enddate)
#                         stage_dict = {stage_obj.id:stage_lst}
#                         final_lst.append(stage_dict)
#                         
#                     else:
#                         stage_lst.append(start_date)
#                         stage_dict = {stage_obj.id:stage_lst}
#                         final_lst.append(stage_dict)
#                         Enddate = start_date
#                 start_date = Enddate + timedelta(days=days)
#                 if start_date.weekday() == 5:
#                     start_date = Enddate + timedelta(days=3)
#                 if start_date.weekday() == 6:
#                     start_date = Enddate + timedelta(days=2)
#         return final_lst
                    
    
    @api.model
    def get_stage_buffer_days(self, args):
        stage_buffer_days = 0
        if 'stage_id' in args:
            try:
                stage_id = int(args['stage_id'])
                stage = self.env['project.task.type'].browse(stage_id)
                stage_buffer_days = stage.buffer_days if stage else 0
            except:
                stage_buffer_days = 0
        return [stage_buffer_days]
    
    @api.onchange('stage_start_date')
    def _compute_end_date(self):
        for record in self:
            if record.stage_start_date and record.stage_id and record.stage_id.buffer_days:
                buffer_days = record.stage_id.buffer_days
                add_days = buffer_days - 1
                for x in range(buffer_days):
                    index = x 
                    Enddate = record.stage_start_date + timedelta(days=index)
                    if Enddate.weekday() in [5,6]:
                        add_days += 1
                    if buffer_days == x + 1:
                        Enddate = record.stage_start_date + timedelta(days=add_days)
                        if Enddate.weekday() in [5,6]:
                            add_days += 1
                Enddate = record.stage_start_date + timedelta(days=add_days)
                record.stage_end_date = Enddate
            if record.stage_start_date and record.stage_id and not record.stage_id.buffer_days:
                record.stage_end_date = record.stage_start_date
                
#     @api.model           
#     def create(self, vals):
#         res = super(ProjectTask, self).create(vals)
#         res.write({'date_start':res.stage_start_date,'date_end':res.stage_end_date})
#         buffer_stages = []
#         stage_objs = self.env['project.task.type'].search([('project_ids','in',[res.project_id.id])], order="sequence asc")
#         schedule_list = False
#         pre_stg_obj = self.env['project.task.stage']
#         if stage_objs:
#             if vals.get('stage_start_date', False) or vals.get('stage_end_date', False) or res.stage_end_date:
#                 schedule_list = self.compute_stages_scheduled( vals.get('stage_end_date') or res.stage_end_date, res)
#             for stage_obj in stage_objs:
#                 if self:
#                     pre_stg_obj = self.env['project.task.stage'].search([('stage_task_id','=',self.id),('stage_id','=',stage_obj.id)])
#                 task_line = {'name':res.name + ' ('+stage_obj.name+')',
#                                                   'stage_task_id':res.id,
#                                                   'stage_id':stage_obj.id,
#                                                   'user_id':res.user_id.id,
#                                                   'stage_start_date':res.stage_start_date,
#                                                   'stage_end_date':res.stage_end_date,
#                                                   'project_id':res.project_id.id,
#                                                   'sequence':stage_obj.sequence,
#                                                   'hide_on_calender':pre_stg_obj.hide_on_calender}
#                 
#                 if schedule_list:
#                     for dct in schedule_list:
#                         if stage_obj.id in dct.keys():
#                             dt_lst = dct.get(stage_obj.id)
#                             task_line.update({'stage_start_date':dt_lst[0],
#                                               'stage_end_date':dt_lst[1]})
#                             continue
#                 buffer_stages.append([0,0,task_line])
#             res.buffer_stage_id = buffer_stages
#         return res

    def write(self, vals):
        if 'planned_duration' in vals and 'date_start' in vals:
            if ' ' in str(vals['date_start']):
                start_date = str(vals['date_start']).split()
                start_date = start_date[0]
            else:
                start_date = vals['date_start']
            vals['stage_start_date'] = str(datetime.strptime(str(start_date),'%Y-%m-%d').date())
            vals['stage_end_date'] = str(datetime.strptime(str(start_date),'%Y-%m-%d').date())
            vals['date_start'] = str(datetime.strptime(str(start_date),'%Y-%m-%d').date())
        if 'date_end' in vals:
            if ' ' in str(vals['date_end']):
                end_date = str(vals['date_end']).split()
                end_date = end_date[0]
            else:
                end_date = vals['date_end']
            vals['stage_end_date'] = str(datetime.strptime(str(end_date),'%Y-%m-%d').date()) if end_date else ''
            vals['date_end'] = str(datetime.strptime(str(end_date),'%Y-%m-%d').date()) if end_date else ''
  
        return super(ProjectTask, self).write(vals)
    
    
#     def write(self, vals):
#         res = super(ProjectTask, self).write(vals) 
#         if vals.get('stage_start_date', False) or vals.get('stage_end_date', False):
#             schedule_list = self.compute_stages_scheduled( vals.get('stage_end_date') or self.stage_end_date, self)
#             for index in schedule_list:
#                 for key, value in index.items():
#                     stage_task = self.env['project.task.stage'].search([
#                         ('stage_id','=',key),
#                         ('stage_task_id','=',self.id)], order="id desc", limit=1)
#                     stage_task.stage_start_date = value[0]
#                     stage_task.stage_end_date = value[1]
#         return res
                
class ProjectTaskType(models.Model):
    _name = "project.task.stage"
    _description = 'Project Task stages'
    
    @api.depends('stage_end_date_calender')
    def _compute_stage_end_date_calender(self):
        for task in self:
            if task.start_date:
                new_date= (datetime.strptime(str(task.end_date), '%Y-%m-%d') + date_utils.relativedelta(days =+ 1))
                task.stage_end_date_calender = new_date
            else:
                task.stage_end_date_calender = False
                
    @api.depends('start_date', 'end_date')
    def _compute_stages_start_date(self):
        for record in self:
            record.is_start_date_exceed = False
            if record.stage_id:
                if record.stage_id == record.stage_task_id.stage_id:
                    if (record.start_date and record.stage_task_id.stage_start_date and record.start_date > record.stage_task_id.stage_start_date) or (record.end_date and record.stage_task_id.stage_end_date and record.end_date < record.stage_task_id.stage_end_date):
                        record.is_start_date_exceed = True
    
    @api.depends('name')
    def _compute_displayname(self):
        for record in self:
            record.display_name = record.name
            if record.stage_task_id.name and record.stage_id.name:
                record.display_name = record.stage_task_id.name + ' ('+record.stage_id.name+')'
                    
    name = fields.Char(related='stage_task_id.name')
    display_name = fields.Char( compute=_compute_displayname)
    stage_id = fields.Many2one('project.task.type')
    user_id = fields.Many2one('res.users')
    stage_task_id = fields.Many2one('project.task')
    project_id = fields.Many2one(related='stage_task_id.project_id')
    start_date  = fields.Date('Stage Start Date', help="Stage Start Date")
    end_date  = fields.Date('Stage End Date', help="Stage End Date")
    sequence = fields.Integer(default=1)
    show_new_stage = fields.Boolean(related='stage_task_id.show_new_stage')
    stage_end_date_calender = fields.Date( compute=_compute_stage_end_date_calender)
    allday = fields.Boolean('All Day', default=True)
    color = fields.Char(default='red')
    is_start_date_exceed = fields.Boolean(compute='_compute_stages_start_date')
    active = fields.Boolean(related='stage_task_id.active')
    hide_on_calender = fields.Boolean("Hide on Calendar", default=False)
    colorpicker = fields.Char(related='stage_id.colorpicker')
    tag_ids = fields.Many2many(related='stage_task_id.tag_ids', string='Tags')
    parent_id = fields.Many2one(related='stage_task_id.parent_id', string='Parent Task')

    def write(self, vals):
        if 'allday' in vals.keys():
            vals.update({'allday':True})
        if self.stage_id == self.stage_task_id.stage_id and 'start_date' in vals.keys() and 'end_date' in vals.keys():
            self.stage_task_id.stage_start_date = vals['start_date']
            self.stage_task_id.stage_end_date = vals['end_date']
        return super(ProjectTaskType, self).write(vals)
    
    
    @api.model
    def get_stage_exceed(self, args):
        exceed = False
        stg = self.search([('name','=',args['stage_name'])], limit=1)
        if stg.stage_task_id.stage_start_date and stg.start_date:
            if stg.stage_task_id.stage_start_date > stg.start_date:
                exceed = True
        return [exceed]

    @api.constrains('start_date')
    def _validate_stage_start_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                pre_seq_records = self.search([('sequence','<',rec.sequence),('stage_task_id','=',rec.stage_task_id.id),('start_date','>',rec.start_date)])
                if pre_seq_records:
                    raise ValidationError(_("%s Stage Start Date / End Date must be bigger than previous stage %s.") % (rec.display_name, pre_seq_records[-1].display_name))
                if rec.start_date > rec.end_date:
                    raise ValidationError(_("Stage Start Date must be less than or equal to Stage End Date."))
        
    @api.constrains('end_date')
    def _validate_stage_end_date(self):
        for rec in self:
            if rec.end_date:
                pre_seq_records = self.search([('sequence','<',rec.sequence),('stage_task_id','=',rec.stage_task_id.id),('end_date','>',rec.end_date)])
                if pre_seq_records:
                    raise ValidationError(_("%s Stage Start Date / End Date must be bigger than previous stage %s.") % (rec.display_name, pre_seq_records[-1].display_name))
                if rec.start_date > rec.end_date:
                    raise ValidationError(_("Stage Start Date must be greater than or equal to Stage End Date."))
    
                
                
class ProjectTaskStages(models.Model):
    _inherit="project.task.type"
    
    colorpicker = fields.Char(string="Color Picker")

