import datetime

from odoo import fields, models, api
from datetime import date, timedelta


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"
    buffer_days = fields.Integer(string="Buffer Days")
    
    
    @api.model
    def create(self, vals):
        res = super(ProjectTaskType, self).create(vals)
        if res.project_ids:
            for project in res.project_ids:
                for task in project.task_ids:
                    task.stage_schedule_ids = [[5,]]
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
                        stage_schedule = self.env['project.task.schedule'].create({'stage_id': stage.id,
                                                                                   'task_id': task.id,
                                                                                   'start_date': start_date,
                                                                                   'end_date': end_date})
                        task_schedule.append(stage_schedule.id)
                    task.stage_schedule_ids = task_schedule
        return res
    
    def write(self, vals):
        res = super(ProjectTaskType, self).write(vals)
        if self.project_ids:
            for project in self.project_ids:
                for task in project.task_ids:
                    task.stage_schedule_ids = [[5,]]
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
                        stage_schedule = self.env['project.task.schedule'].create({'stage_id': stage.id,
                                                                                   'task_id': task.id,
                                                                                   'start_date': start_date,
                                                                                   'end_date': end_date})
                        task_schedule.append(stage_schedule.id)
                    task.stage_schedule_ids = task_schedule
        return res

    @api.onchange("buffer_days")
    def onchange_buffer_days(self):
        tasks = self.env['project.task'].search([])
        all_stages = self.env['project.task.type'].search([], order='sequence asc')
        day_diff, last_task = None, None
        for stage in all_stages:
            for o_task in tasks:
                set_tasks = self.env['project.task.schedule'].search([('task_id','=',o_task.id)])
                for task in set_tasks:
                    if task.task_id:
                        if task.stage_id.sequence == stage.sequence and task.task_id.project_id.id in stage.project_ids.ids:
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
                                task.start_date = last_task.end_date + timedelta(days=1)
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


class ProjectTaskSchedule(models.Model):
    _name = "project.task.schedule"
    _description = "Task Stage Schedule"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    stage_id = fields.Many2one("project.task.type", string="Stage Name")
    task_id = fields.Many2one("project.task")


class ProjectTask(models.Model):
    _inherit = "project.task"

    stage_schedule_ids = fields.Many2many("project.task.schedule", string="Stage Name",
                                          domain="[('task_id' , '=' , id)]", ondelete='cascade')

    @api.model
    def create(self, data):
        rec = super(ProjectTask, self).create(data)
        stages = [i for i in self.env['project.task.type'].search([('project_ids','in',[rec.project_id.id])],
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
            stage_schedule = self.env['project.task.schedule'].create({'stage_id': stage.id,
                                                                       'task_id': rec.id,
                                                                       'start_date': start_date,
                                                                       'end_date': end_date})
            task_schedule.append(stage_schedule.id)
        rec.stage_schedule_ids = task_schedule
        return rec

    @api.onchange("stage_schedule_ids")
    def onchange_task_type(self):
        last_stage = None
        for stage in self.stage_schedule_ids:
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
