# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    @api.model
    def get_manufacture_orders(self, employee=False):
        employee_id = self.env['hr.employee'].browse(employee)
        wc_values = []
        wc_values.append({'id': employee_id.primary_wc_id.id, 'name': employee_id.primary_wc_id.name})
        wc_values.append({'id': employee_id.secondary_wc_id.id, 'name': employee_id.secondary_wc_id.name})
        wc_values.append({'id': employee_id.tertiary_wc_id.id, 'name': employee_id.tertiary_wc_id.name})

        mo_ids = []
        for each in wc_values:
            mo_id = self.env["mrp.workcenter"].browse(each["id"]).order_ids.mapped("production_id")
            if mo_id:
                mo_ids.append(mo_id)
        # if not self.env.user.workcenter_id.order_ids:
        #     return False
        # mo_ids = self.env.user.workcenter_id.order_ids.mapped('production_id')
        # if employee:
        #     employee = self.env['hr.employee'].browse(employee)
        #     if employee:
        #         job_cost = self.env['job.cost'].search([('employee_id', '=', employee.id), ('check_out', '=', False)], limit=1)
        #         if job_cost.manufacture_id:
        #             mo_ids = mo_ids.filtered(lambda x: x.id == job_cost.manufacture_id.id)
        mo_values = []
        for each in mo_ids:
            vals = {'id': each.id, 'name': each.name}
            mo_values.append(vals)
        return mo_values


class WorkcenterProduction(models.Model):
    _inherit = 'mrp.workcenter'

    @api.model
    def get_workcenter(self, employee=False):
        employee_id = self.env['hr.employee'].browse(employee)
        wc_values = []
        wc_values.append({'id': employee_id.primary_wc_id.id, 'name': employee_id.primary_wc_id.name})
        wc_values.append({'id': employee_id.secondary_wc_id.id, 'name': employee_id.secondary_wc_id.name})
        wc_values.append({'id': employee_id.tertiary_wc_id.id, 'name': employee_id.tertiary_wc_id.name})
        return wc_values