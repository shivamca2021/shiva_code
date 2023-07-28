from odoo import  models,api

class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """
        Performs a search_read and a search_count.

        :param domain: search domain
        :param fields: list of fields to read
        :param limit: maximum number of records to read
        :param offset: number of records to skip
        :param order: columns to sort results
        :return: {
            'records': array of read records (result of a call to 'search_read')
            'length': number of records matching the domain (result of a call to 'search_count')
        }
        """
        if self.env.context.get('duplicate'):
            domain = self.with_context(duplicate_read=True).action_duplicate_contacts()
        records = self.search_read(domain, fields, offset=offset, limit=limit, order=order)
        if not records:
            return {
                'length': 0,
                'records': []
            }
        if limit and (len(records) == limit or self.env.context.get('force_search_count')):
            length = self.search_count(domain)
        else:
            length = len(records) + offset
        new_records, new_records1, checked = [], [], False
        if records and self.env.context.get('started_with') and self.env.context.get('started') or self.env.context.get('ended'):
            started_domain = self.env.context.get('started')
            ended_domain = self.env.context.get('ended')
            for line in records:
                line_field_list=[]
                # model = []
                new_line = self.sudo().browse(line.get('id')).read()
                if started_domain and len(started_domain[0]) == 3:
                    field_name, field_value = started_domain[0][0], started_domain[0][2].lower()
                    if type(new_line[0][field_name]) == list:
                        model = self.env['ir.model'].sudo().search([('model', '=', self._name)])
                        relations = self.env['ir.model.fields'].sudo().search([('model_id','=', model.id),('name','=',field_name)])
                        for id in new_line[0][field_name]:
                            model=self.env[relations.relation].sudo().browse(id)
                            rec_name =model._rec_name
                            read_model = model.read()
                            line_field_list.append(read_model[0][rec_name])
                    elif type(new_line[0][field_name]) == tuple:
                        if '/' in new_line[0][field_name][1]:
                            line_field_list.append(new_line[0][field_name][1].split('/ ')[1])
                        else:
                            line_field_list.append(new_line[0][field_name][1])
                    else:
                        line_field_list.append(new_line[0][field_name])
                    for line_field in line_field_list:
                        if line_field.lower().startswith(field_value):
                            new_records.append(line)
                if not new_records and ended_domain and len(ended_domain[0]) == 3:
                    e_field_name, e_field_value = ended_domain[0][0], ended_domain[0][2].lower()
                    checked = True
                    if type(new_line[0][e_field_name]) == list:
                        model = self.env['ir.model'].sudo().search([('model', '=', self._name)])
                        relations = self.env['ir.model.fields'].sudo().search([('model_id','=', model.id),('name','=',e_field_name)])
                        for id in new_line[0][e_field_name]:
                            model=self.env[relations.relation].sudo().browse(id)
                            rec_name =model._rec_name
                            read_model = model.read()
                            line_field_list.append(read_model[0][rec_name])
                    elif type(new_line[0][e_field_name]) == tuple:
                        if '/' in new_line[0][e_field_name][1]:
                            line_field_list.append(new_line[0][e_field_name][1].split('/ ')[1])
                        else:
                            line_field_list.append(new_line[0][e_field_name][1])
                    else:
                        line_field_list.append(new_line[0][e_field_name])
                    for e_line_field in line_field_list:
                        if e_line_field.lower().endswith(e_field_value):
                            new_records.append(line)
            if not checked and new_records and ended_domain and len(ended_domain[0]) == 3:
                for line in new_records:
                    line_field_list = []
                    new_line = self.sudo().browse(line.get('id')).read()
                    e_field_name, e_field_value = ended_domain[0][0], ended_domain[0][2].lower()
                    checked = True
                    if type(new_line[0][e_field_name]) == list:
                        model = self.env['ir.model'].sudo().search([('model', '=', self._name)])
                        relations = self.env['ir.model.fields'].sudo().search(
                            [('model_id', '=', model.id), ('name', '=', e_field_name)])
                        for id in new_line[0][e_field_name]:
                            model = self.env[relations.relation].sudo().browse(id)
                            rec_name = model._rec_name
                            read_model = model.read()
                            line_field_list.append(read_model[0][rec_name])
                    elif type(new_line[0][e_field_name]) == tuple:
                        if '/' in new_line[0][e_field_name][1]:
                            line_field_list.append(new_line[0][e_field_name][1].split('/ ')[1])
                        else:
                            line_field_list.append(new_line[0][e_field_name][1])
                    else:
                        line_field_list.append(new_line[0][e_field_name])
                    for e_line_field in line_field_list:
                        if e_line_field.lower().endswith(e_field_value):
                            new_records.append(line)
                new_records = new_records1

        if new_records:
            records = new_records
            length = len(records)
        return {
            'length': length,
            'records': records
        }