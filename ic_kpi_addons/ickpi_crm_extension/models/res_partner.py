# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

CREDITS = [
    ('great', 'Great'),
    ('good', 'Good'),
    ('average', 'Average'),
    ('late', 'Late'),
    ('always_late', 'Always Late'),
]


class PartnerExtended(models.Model):
    _inherit = 'res.partner'

    def _default_category(self):
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    sic_code = fields.Char("SIC")
    parent_company = fields.Char("Parent Company")
    fax_number = fields.Char("Fax Number")
    no_of_employee = fields.Char("Number of Employee")
    year_establishment = fields.Char("Year Establishment")
    assigned_cs = fields.Many2one("res.employee", "Assigned CS")
    structure_id = fields.Many2one("ickpi.structure", "Structure")
    annual_sales = fields.Many2one("ickpi.sales", "Annual Sales")

    category_id = fields.Many2many('res.partner.category', column1='partner_id',
                                    column2='category_id', string='Types', default=_default_category)

    # new fields
    contact_type = fields.Many2one("contact.type", "Contact Type")
    private_Mail = fields.Char("Private Email")
    Private_mo = fields.Char("Private Mobile")
    reports_to = fields.Char("Report to [Manager]")
    joined_company = fields.Date("Joined The Company")
    birth_date = fields.Date("Birth Date")

    spouse_name = fields.Char("Spouse Name")
    anniversary = fields.Date("Anniversary")
    num_children = fields.Integer("Number of Children")
    Children_name = fields.Char("Name of Children")

    home_address_1 = fields.Char("Address Line 1")
    home_address_2 = fields.Char("Address Line 2")
    home_city = fields.Char("City")
    home_sate = fields.Many2one("res.country.state", 'State')
    home_zip = fields.Integer("Zip")
    home_country = fields.Many2one("res.country", "Country")

    year_registered = fields.Integer("Year of registration")
    credit_rate = fields.Selection(CREDITS, "Credit Rate")
    credit_term = fields.Char("Credit Term")
    credit_limit = fields.Float("Credit Limit")

    primary_discount = fields.Float('Primary Discount %')
    special_discount = fields.Float('Special Discount %')

    fax = fields.Char('Fax')
    is_parent = fields.Boolean('Is this a Parent Company')
    parent_company_id = fields.Many2one('res.partner', 'Prent Company')
    cs_rep_id = fields.Many2one('hr.employee', 'Assigned CS Rep')
    year_sales = fields.Selection([('less', 'Less Then 1M'),
                                   ('1_3', '1-3M'),
                                   ('4_8', '4-8M'),
                                   ('9_15', '9-15M'),
                                   ('15_25', '15-25M'),
                                   ('over', 'Over 25M')], string='Annual Sales')
    no_emp = fields.Selection([('0_20', '0-20'),
                               ('21_40', '21-40'),
                               ('41_60', '41-60'),
                               ('60_100', '60-100'),
                               ('100_200', '100-200'),
                               ('200_300', '200-300'),
                               ('300', '300+')], string='Range of Employees')
    year_registered = fields.Integer('Year of Registration')
    sic_code = fields.Char('SIC Code')
    sic_status = fields.Char('CNC Status')
    inds_membership = fields.Char('Industry Membership')
    cnc_type = fields.Char('CNC Type/Machine Type')
    company_creation_date = fields.Date("Creation Date")
    last_activity_date = fields.Date("Last Activity Date")
    current_software = fields.Char('Current Software')
    buy_rating = fields.Char('Buy Rating')
    old_sales_person = fields.Char('Old Account Owner/Sales Person')
    no_emp_count = fields.Char('#Employees')
    annual_revenue = fields.Char('Annual Revenue USD')
    annual_rev_currency = fields.Char('Annual Revenue Currency')
    source_id = fields.Many2one('utm.source', 'Source')


class Structure(models.Model):
    _name = "ickpi.structure"
    
    name = fields.Char("Name")


class AnnualSales(models.Model):
    _name = "ickpi.sales"
    
    name = fields.Char("Name")


class ContactType(models.Model):
    _name = "contact.type"
    
    name = fields.Char("Name")
