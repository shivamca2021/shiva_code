from odoo import api, fields, models, _
from datetime import date, timedelta
import datetime


class ProjectStage(models.Model):
    _inherit = "project.task.type"
    _description = 'Project Task Type'
    
    buffer_days = fields.Integer( string='Buffer Days')
    
    @api.model
    def create(self, vals):
        res = super(ProjectStage, self).create(vals)
        if res.project_ids:
            for project in res.project_ids:
                for task in project.task_ids:
                    task.buffer_stage_id = [[5,]]
                    stages = [i for i in self.env['project.task.type'].search([('project_ids','in',res.project_ids.ids)],
                                                                  order='sequence asc')]
                    task_schedule, start_date, end_date, previous_task, stage_schedule = [], None, None, None, None
                    for stage in stages:
                        if not (start_date and end_date):
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
                        stage_schedule = self.env['project.task.stage'].create({'name':task.name + ' ('+stage.name+')',
                                                  'stage_task_id':task.id,
                                                  'stage_id':stage.id,
                                                  'start_date':start_date,
                                                  'end_date':end_date,
                                                  'user_id':task.user_id.id,
                                                  'project_id':task.project_id.id,
                                                  'sequence':stage.sequence})
                        task_schedule.append(stage_schedule.id)
                    task.buffer_stage_id = task_schedule
        return res
    
    def write(self, vals):
        res = super(ProjectStage, self).write(vals)
        if self.project_ids:
            for project in self.project_ids:
                for task in project.task_ids:
                    task.buffer_stage_id = [[5,]]
                    stages = [i for i in self.env['project.task.type'].search([('project_ids','in',self.project_ids.ids)],
                                                                  order='sequence asc')]
                    task_schedule, start_date, end_date, previous_task, stage_schedule = [], None, None, None, None
                    for stage in stages:
                        if not (start_date and end_date):
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
                        stage_schedule = self.env['project.task.stage'].create({'name':task.name + ' ('+stage.name+')',
                                                  'stage_task_id':task.id,
                                                  'stage_id':stage.id,
                                                  'start_date':start_date,
                                                  'end_date':end_date,
                                                  'user_id':task.user_id.id,
                                                  'project_id':task.project_id.id,
                                                  'sequence':stage.sequence})
                        task_schedule.append(stage_schedule.id)
                    task.buffer_stage_id = task_schedule
        return res

    @api.onchange("buffer_days")
    def onchange_buffer_days(self):
        tasks = self.env['project.task'].search([])
        all_stages = self.env['project.task.type'].search([], order='sequence asc')
        day_diff, last_task = None, None
        for stage in all_stages:
            for o_task in tasks:
                set_tasks = self.env['project.task.stage'].search([('stage_task_id','=',o_task.id)])
                for task in set_tasks:
                    if task.stage_task_id:
                        if task.stage_id.sequence == stage.sequence and task.stage_task_id.project_id.id in stage.project_ids.ids:
                            if self._origin.sequence == stage.sequence:
                                day_diff = self.buffer_days - task.stage_id.buffer_days
                                task.end_date = task.start_date + timedelta(days=self.buffer_days)
                                total_days = [task.start_date + timedelta(x + 1) for x in range((task.end_date - task.start_date).days + 1)]
                                off_days = sum(1 for day in total_days if day.weekday() >= 5)
                                if off_days:
                                    task.end_date = task.start_date + timedelta(days=self.buffer_days + off_days + 1)
                                if task.end_date.weekday() == 5:
                                    task.end_date += timedelta(days=2)
                                elif task.end_date.weekday() == 6:
                                    task.end_date += timedelta(days=1)
                                last_task = task
                            elif self._origin.sequence < stage.sequence:
                                last_task = set_tasks[-1]
                                task.start_date = last_task.end_date #+ timedelta(days=1)
                                task.end_date = task.start_date + timedelta(days=stage.buffer_days)
                                if task.start_date.weekday() == 5:
                                    task.start_date += timedelta(days=2)
                                elif task.start_date.weekday() == 6:
                                    task.start_date += timedelta(days=1)
                                total_days = [task.start_date + timedelta(x + 1) for x in
                                              range((task.end_date - task.start_date).days)]
                                off_days = sum(1 for day in total_days if day.weekday() >= 5)
                                if off_days:
                                    task.end_date = task.start_date + timedelta(days=stage.buffer_days + off_days)
                                if task.end_date.weekday() == 5:
                                    task.end_date += timedelta(days=2)
                                elif task.end_date.weekday() == 6:
                                    task.end_date += timedelta(days=1)
                                last_task = task

#     @api.model
#     def create(self, vals):
#         res = super(ProjectStage, self).create(vals)
#         if res.project_ids:
#             for project in res.project_ids:
#                 for task in project.task_ids:
#                     if task.stage_end_date:
#                         buffer_stages = []
#                         sch_list = task.compute_stages_scheduled(task.stage_end_date, task)
#                         task.buffer_stage_id = [[5,]]
#                         for index in sch_list:
#                             for key, value in index.items():
#                                 task_stage_ids = task.buffer_stage_id.mapped('stage_id').ids
#                                 if key not in task_stage_ids:
#                                     stage = self.env['project.task.type'].browse(key)
#                                     task_line = {'name':task.name + ' ('+stage.name+')',
#                                                   'stage_task_id':task.id,
#                                                   'stage_id':stage.id,
#                                                   'stage_start_date':value[0],
#                                                   'stage_end_date':value[1],
#                                                   'user_id':task.user_id.id,
#                                                   'project_id':task.project_id.id,
#                                                   'sequence':stage.sequence}
#                                     buffer_stages.append([0,0,task_line])
#                         task.write({'buffer_stage_id':buffer_stages})
#         return res
# 
#     def write(self, vals):
#         buffer_stages = []
#         res = super(ProjectStage, self).write(vals)
#         if self.project_ids:
#             for project in self.project_ids:
#                 for task in project.task_ids:
#                     if task.stage_end_date:
#                         buffer_stages = []
#                         sch_list = task.compute_stages_scheduled(task.stage_end_date, task)
#                         task.buffer_stage_id = [[5,]]
#                         for index in sch_list:
#                             for key, value in index.items():
#                                 task_stage_ids = task.buffer_stage_id.mapped('stage_id').ids
#                                 if key not in task_stage_ids:
#                                     stage = self.env['project.task.type'].browse(key)
#                                     task_line = {'name':task.name + ' ('+stage.name+')',
#                                                   'stage_task_id':task.id,
#                                                   'stage_id':stage.id,
#                                                   'stage_start_date':value[0],
#                                                   'stage_end_date':value[1],
#                                                   'user_id':task.user_id.id,
#                                                   'project_id':task.project_id.id,
#                                                   'sequence':stage.sequence}
#                                     buffer_stages.append([0,0,task_line])
#                         task.write({'buffer_stage_id':buffer_stages})
#         return res
