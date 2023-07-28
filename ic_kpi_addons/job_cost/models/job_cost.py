# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _
from odoo.tools import format_datetime

class JobCost(models.Model):
    _name = 'job.cost'
    _description = 'Job Cost'
    _inherit = ['mail.thread']
    _order = "check_in desc"

    def _default_employee(self):
        return self.env.user.employee_id

    employee_id = fields.Many2one('hr.employee', string="Employee", default=_default_employee, required=True, ondelete='cascade', index=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string="Work Center", ondelete='cascade', index=True)
    manufacture_id = fields.Many2one('mrp.production', string="Manufacturing Order")
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=True)
    check_out = fields.Datetime(string="Check Out")
    cost = fields.Float(string="Cost", default=0.0, compute='_compute_cost', store=True)
    worked_hours = fields.Float(string='Worked Hours', compute='_compute_worked_hours', store=True, readonly=True)

    @api.depends('employee_id','worked_hours')
    def _compute_cost(self):
        for jobcost in self:
            if jobcost.employee_id:
                jobcost.cost = jobcost.employee_id.timesheet_cost * jobcost.worked_hours

    def name_get(self):
        result = []
        for jobcost in self:
            if not jobcost.check_out:
                result.append((jobcost.id, _("%(empl_name)s from %(check_in)s") % {
                    'empl_name': jobcost.employee_id.name,
                    'check_in': format_datetime(self.env, jobcost.check_in, dt_format=False),
                }))
            else:
                result.append((jobcost.id, _("%(empl_name)s from %(check_in)s to %(check_out)s") % {
                    'empl_name': jobcost.employee_id.name,
                    'check_in': format_datetime(self.env, jobcost.check_in, dt_format=False),
                    'check_out': format_datetime(self.env, jobcost.check_out, dt_format=False),
                }))
        return result

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for jobcost in self:
            if jobcost.check_out and jobcost.check_in:
                delta = jobcost.check_out - jobcost.check_in
                jobcost.worked_hours = delta.total_seconds() / 3600.0
            else:
                jobcost.worked_hours = False

    @api.constrains('check_in', 'check_out')
    def _check_validity_check_in_check_out(self):
        """ verifies if check_in is earlier than check_out. """
        for jobcost in self:
            if jobcost.check_in and jobcost.check_out:
                if jobcost.check_out < jobcost.check_in:
                    raise exceptions.ValidationError(_('"Check Out" time cannot be earlier than "Check In" time.'))

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the jobcost attendance record compared to the others from the same employee.
            For the same employee we must have :
                * maximum 1 "open" jobcost attendance record (without check_out)
                * no overlapping time slices with previous employee records
        """
        for jobcost in self:
            # we take the latest jobcost attendance before our check_in time and check it doesn't overlap with ours
            last_jobcost_attendance_before_check_in = self.env['job.cost'].search([
                ('employee_id', '=', jobcost.employee_id.id),
                ('check_in', '<=', jobcost.check_in),
                ('id', '!=', jobcost.id),
            ], order='check_in desc', limit=1)
            if last_jobcost_attendance_before_check_in and last_jobcost_attendance_before_check_in.check_out and last_jobcost_attendance_before_check_in.check_out > jobcost.check_in:
                raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                    'empl_name': jobcost.employee_id.name,
                    'datetime': format_datetime(self.env, jobcost.check_in, dt_format=False),
                })

            if not jobcost.check_out:
                # if our jobcost attendance is "open" (no check_out), we verify there is no other "open" attendance
                no_check_out_jobcost_attendances = self.env['job.cost'].search([
                    ('employee_id', '=', jobcost.employee_id.id),
                    ('check_out', '=', False),
                    ('id', '!=', jobcost.id),
                ], order='check_in desc', limit=1)
                if no_check_out_jobcost_attendances:
                    raise exceptions.ValidationError(_("Cannot create new jobcost attendance record for %(empl_name)s, the employee hasn't checked out since %(datetime)s") % {
                        'empl_name': jobcost.employee_id.name,
                        'datetime': format_datetime(self.env, no_check_out_jobcost_attendances.check_in, dt_format=False),
                    })
            else:
                # we verify that the latest jobcost attendance with check_in time before our check_out time
                # is the same as the one before our check_in time computed before, otherwise it overlaps
                last_jobcost_attendance_before_check_out = self.env['job.cost'].search([
                    ('employee_id', '=', jobcost.employee_id.id),
                    ('check_in', '<', jobcost.check_out),
                    ('id', '!=', jobcost.id),
                ], order='check_in desc', limit=1)
                if last_jobcost_attendance_before_check_out and last_jobcost_attendance_before_check_in != last_jobcost_attendance_before_check_out:
                    raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                        'empl_name': jobcost.employee_id.name,
                        'datetime': format_datetime(self.env, last_jobcost_attendance_before_check_out.check_in, dt_format=False),
                    })

    @api.returns('self', lambda value: value.id)
    def copy(self):
        raise exceptions.UserError(_('You cannot duplicate an attendance.'))
