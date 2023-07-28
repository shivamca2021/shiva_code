from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'
   
    def partner_import_file(self):
        import_record = self.env['base_import.import'].create({
                    'res_model': 'res.partner',
                    'file':  self.customer_import,
                    'file_type': self.customer_import_file_type,
                    'file_name': self.customer_import_name,
                })
        results = import_record.do(
               ['name','parent_id','child_ids/name', 'street', 'street2', 'city', 'zip', 'fax', 'mobile', 'email', 'phone', 'state_id', 
 'country_id','website','category_id'],
               [],
                {'headers': True, 'advanced': True, 'keep_matches': False, 'name_create_enabled_fields': {'parent_id': True, 
 'child_ids/contact_type': True, 'category_id': True}, 'skip': 0, 'limit': 
2000, 'encoding': '', 'separator': ',', 'quoting': '"', 'sheet': '', 'date_format': '', 'datetime_format': '', 
'float_thousand_separator': ',', 'float_decimal_separator': '.', 'fields': []},
               False
           )
        
        return results
    
    def partner_vendor_import_file(self):
        import_record = self.env['base_import.import'].create({
                    'res_model': 'res.partner',
                    'file':  self.vendor_import,
                    'file_type': self.vendor_import_file_type,
                    'file_name': self.vendor_import_name,
                })
        results = import_record.do(
               ['name','parent_id','child_ids/name', 'street', 'street2', 'city', 'zip', 'fax', 'mobile', 'email', 'phone', 'state_id', 
 'country_id','website','category_id'],
               [],
                {'headers': True, 'advanced': True, 'keep_matches': False, 'name_create_enabled_fields': {'parent_id': True, 
 'child_ids/contact_type': True, 'category_id': True}, 'skip': 0, 'limit': 
2000, 'encoding': '', 'separator': ',', 'quoting': '"', 'sheet': '', 'date_format': '', 'datetime_format': '', 
'float_thousand_separator': ',', 'float_decimal_separator': '.', 'fields': []},
               False
           )
        
        return results

    def partner_employee_import_file(self):
        import_record = self.env['base_import.import'].create({
                    'res_model': 'hr.employee',
                    'file':  self.employee_import,
                    'file_type': self.employee_import_file_type,
                    'file_name': self.employee_import_name,
                })
        results = import_record.do(
               ['name', 'job_id', 'department_id', 'parent_id', 'mobile_phone', 'work_phone', 'work_email', 
 'coach_id', 'marital', 'country_id', 'identification_id', 'passport_id', 'gender', 'birthday', 'place_of_birth', 
 'country_of_birth', 'children', 'permit_no', 'visa_no', 'visa_expire', 'category_ids'],
               [],
                {'headers': True, 'advanced': True, 'keep_matches': False, 'name_create_enabled_fields': {'parent_id': True, 
 'child_ids/contact_type': True, 'category_ids': True}, 'skip': 0, 'limit': 
2000, 'encoding': '', 'separator': ',', 'quoting': '"', 'sheet': '', 'date_format': '%Y-%m-%d', 'datetime_format': '', 
'float_thousand_separator': ',', 'float_decimal_separator': '.', 'fields': []},
               False
           )
        _logger.info('importing %d rows...', results)
        return results

    def user_import_data(self):
        vals = []
        for user_info in self.user_info_ids:
            data = {'name': user_info.name, 'login': user_info.email, 'password': user_info.passwd}
            vals.append(data)
        return self.env['res.users'].create(vals)

    def company_import_data(self):
        vals = {'name': self.name,
                'email': self.email,
                'phone': self.phone,
                'street': self.street,
                'street2': self.street2,
                'city': self.city,
                'zip': self.zip,
                'state_id': self.state_id.id,
                'country_id': self.country_id.id,
                'logo': self.image_1920,
                'favicon': self.image_1920
                }
        return self.env['res.company'].create(vals)
