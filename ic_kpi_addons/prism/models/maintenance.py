# -*- coding: utf-8 -*-
from odoo import fields, models, api


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    purchase_date = fields.Date("Purchase Date")
    place_of_purchase = fields.Char("Place of Purchase")
    function_of_machine = fields.Char("Function of Machine")
    machine_capacity = fields.Integer("Capacity of Machine # Parts")
    set_up_time = fields.Float("Set Up Time")
