# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions, _, SUPERUSER_ID


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    job_attendance_ids = fields.One2many('job.cost', 'employee_id', help='list of attendances for the employee')
    job_attendance_state = fields.Selection(string="Job Attendance Status", compute='_compute_job_attendance_state', selection=[('checked_out', "Checked out"), ('checked_in', "Checked in")])
    last_job_attendance_id = fields.Many2one('job.cost', compute='_compute_last_job_attendance_id', store=True)
    last_job_check_in = fields.Datetime(related='last_job_attendance_id.check_in', store=True)
    last_job_check_out = fields.Datetime(related='last_job_attendance_id.check_out', store=True)
    job_hours_today = fields.Float(compute='_compute_job_hours_today')

    def _compute_job_hours_today(self):
        now = fields.Datetime.now()
        now_utc = pytz.utc.localize(now)
        for employee in self:
            # start of day in the employee's timezone might be the previous day in utc
            tz = pytz.timezone(employee.tz)
            now_tz = now_utc.astimezone(tz)
            start_tz = now_tz + relativedelta(hour=0, minute=0)  # day start in the employee's timezone
            start_naive = start_tz.astimezone(pytz.utc).replace(tzinfo=None)

            attendances = self.env['job.cost'].search([
                ('employee_id', '=', employee.id),
                ('check_in', '<=', now),
                '|', ('check_out', '>=', start_naive), ('check_out', '=', False),
            ])

            worked_hours = 0
            for attendance in attendances:
                delta = (attendance.check_out or now) - max(attendance.check_in, start_naive)
                worked_hours += delta.total_seconds() / 3600.0
            employee.job_hours_today = worked_hours

    @api.depends('last_job_attendance_id.check_in', 'last_job_attendance_id.check_out', 'last_job_attendance_id')
    def _compute_job_attendance_state(self):
        for employee in self:
            att = employee.last_job_attendance_id.sudo()
            employee.job_attendance_state = att and not att.check_out and 'checked_in' or 'checked_out'

    @api.depends('job_attendance_ids')
    def _compute_last_job_attendance_id(self):
        for employee in self:
            employee.last_job_attendance_id = self.env['job.cost'].search([
                ('employee_id', '=', employee.id),
            ], limit=1)

    def job_attendance_manual(self, next_action, mo_id=False, entered_pin=None):
        self.ensure_one()
        can_check_without_pin = not self.env.user.has_group('hr_attendance.group_hr_attendance_use_pin') or (self.user_id == self.env.user and entered_pin is None)
        if can_check_without_pin or entered_pin is not None and entered_pin == self.sudo().pin:
            workcenter = self.env.user.workcenter_id.id
            return self._job_attendance_action(next_action, workcenter, mo_id)
        return {'warning': _('Wrong PIN')}

    def _job_attendance_action(self, next_action, workcenter=False, mo_id=False):
        """ Changes the attendance of the employee.
            Returns an action to the check in/out message,
            next_action defines which menu the check in/out message should return to. ("My Attendances" or "Kiosk Mode")
        """
        self.ensure_one()
        employee = self.sudo()
        action_message = self.env["ir.actions.actions"]._for_xml_id("hr_attendance.hr_attendance_action_greeting_message")
        action_message['previous_attendance_change_date'] = employee.last_job_attendance_id and (employee.last_job_attendance_id.check_out or employee.last_job_attendance_id.check_in) or False
        action_message['employee_name'] = employee.name
        action_message['barcode'] = employee.barcode
        action_message['next_action'] = next_action
        action_message['job_hours_today'] = employee.job_hours_today
        if employee.user_id:
            modified_attendance = employee.with_user(employee.user_id)._job_attendance_action_change(workcenter, mo_id)
        else:
            modified_attendance = employee._job_attendance_action_change(workcenter, mo_id)
        action_message['attendance'] = modified_attendance.read()[0]
        return {'action': action_message}

    def _job_attendance_action_change(self, workcenter, mo_id):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        self.ensure_one()
        action_date = fields.Datetime.now()

        if self.job_attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
                'workcenter_id': workcenter,
                'manufacture_id': mo_id,
            }
            return self.env['job.cost'].create(vals)
        attendance = self.env['job.cost'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        if attendance:
            attendance.check_out = action_date
        else:
            raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.sudo().name, })
        return attendance


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    primary_wc_id = fields.Many2one('mrp.workcenter', string='Primary WC')
    secondary_wc_id = fields.Many2one('mrp.workcenter', string='Secondary WC')
    tertiary_wc_id = fields.Many2one('mrp.workcenter', string='Tertiary WC')

