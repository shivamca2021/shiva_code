import odoo
from odoo.api import Environment
from odoo import fields, models, api, _
import xmlrpc.client

class ServerInstance(models.Model):
    _name = 'server.instance'

    name = fields.Char("Name")
    ip_address = fields.Char("IP Address")
    host_name = fields.Char("Host Name")
    db_name = fields.Char("Database Name")
    user_name = fields.Char("User Name")
    password = fields.Char("Password")

class TransferRecord(models.Model):
    _name = 'transfer.record'

    server_id = fields.Many2one("server.instance", "Server Instance")
    model_id = fields.Many2one("res.model", "Model")
    record_ids = fields.Char("Record Ids")

    def transfer_record(self):
        model_id = self.env['ir.model'].search([('model', '=', self.env.context.get('res_model'))], limit=1)
        self.model_id = model_id.id
        self.record_ids = self.env.context.get('res_ids')
        record_ids = list(self.env.context.get('res_ids'))
        self.moveContatcRecord(self.server_id, model_id, record_ids)
        return True

    def moveContatcRecord(self, server_id, model_id, record_ids):
        db = odoo.sql_db.db_connect(server_id.db_name)
        with db.cursor() as newcr:
            environment = Environment(newcr, odoo.SUPERUSER_ID, {})
            for rec in self.env[model_id.model].browse(record_ids):
                vals = rec.with_context(active_test=False).copy_data()[0]
                values = {}
                for key in environment[model_id.model]._fields.keys():
                    if key in vals.keys():
                        if environment[model_id.model]._fields[key].type == 'many2one' and environment[model_id.model]._fields[key].comodel_name != '_unknown':
                            comodel = environment[model_id.model]._fields[key].comodel_name
                            cmodel_id = environment['ir.model'].search([('model', '=', comodel)])
                            if len(cmodel_id) > 1:
                                cmodel_rec = environment[comodel].search([('id', '=', vals[key])])
                                if len(cmodel_rec) > 1:
                                    values.update({key: vals[key]})
                        elif environment[model_id.model]._fields[key].type in ('many2many') and environment[model_id.model]._fields[key].comodel_name != '_unknown':
                            comodel = environment[model_id.model]._fields[key].comodel_name
                            cmodel_id = environment['ir.model'].search([('model', '=', comodel)])
                            if len(cmodel_id) > 1:
                                cmodel_rec = environment[comodel].search([('id', 'in', vals[key][0][2])])
                                if len(cmodel_rec) > 1:
                                    values.update({key: [(6, 0, cmodel_rec.ids)]})
                        else:
                            values.update({key: vals[key]})
                values['user_id'] = False
                environment[model_id.model].with_context(lang=None).create(values)
        return True