from odoo import api, fields, models, _

class Salesperson(models.TransientModel):
    _name = 'salesperson.wizard'

    salesperson_id = fields.Many2one("res.users", "Assign Salesperson")

    def action_add_salesperson(self):
        for record in self:
            contact_ids = self.env['res.partner'].browse(self.env.context.get('active_ids'))
            print(record)
            for contact in contact_ids:
                contact.write({'user_id':self.salesperson_id.id})
            return True

