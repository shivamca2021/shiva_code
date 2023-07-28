# -*- coding: utf-8 -*-

from odoo import fields, models, api


class PartnerInfo(models.Model):
    _inherit = 'res.partner'

    user_info_ids = fields.One2many('user.info' ,'partner_id', string="User Info")
    customer_import = fields.Binary('File', help="File to check and/or import, raw binary (not base64)", attachment=False)
    customer_import_name = fields.Char(string="Customer Details Filename")
    customer_import_file_type = fields.Char('File Type')
    vendor_import = fields.Binary('File', help="File to check and/or import, raw binary (not base64)", attachment=False)
    vendor_import_name = fields.Char(string="Vendor Details Filename")
    vendor_import_file_type = fields.Char('File Type')
    chartofacc_import = fields.Binary(string="Chart of Account Details")
    chartofacc_import_name = fields.Char(string="Chart of Account Details Filename")
    chartofacc_import_file_type = fields.Char('File Type')
    employee_import = fields.Binary('File', help="File to check and/or import, raw binary (not base64)", attachment=False)
    employee_import_name = fields.Char(string="Employee Details Filename")
    employee_import_file_type = fields.Char('File Type')

 
class UserInfo(models.Model):
    _name = 'user.info'
    _description = "User Information"

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    passwd = fields.Char(string="Password")
    is_admin = fields.Boolean(string="Is Admin")
    partner_id = fields.Many2one('res.partner', string="Partner")
