from odoo import api, fields, models, _

class PartsWidthWizard(models.TransientModel):
    _name = 'parts.width.wizard'
    _description = 'Parts width Wizard'


    w_part_id = fields.Many2one('parts', 'Part')
    w_operator_selection = fields.Selection([('+', '+'), ('-', '-'), ('*', '*'),('/', '/'),('=', '=')], string="Operator")
    w_formula_id = fields.Many2one('formula.variable', string="Formula")
    is_w_formula_fixed_size = fields.Boolean(string='Formula Fixed Size', related="w_formula_id.is_fixed_size")
    w_formula_fixed_size = fields.Float(string="Fixed Size")

    # def width_part_line(self):
    #     if self.w_part_id and self.w_formula_id and self.w_operator_selection:
    #         formula = self.w_formula_id.name
    #         if self.w_formula_id.is_fixed_size:
    #             formula = str(self.w_formula_fixed_size)
    #         self.w_part_id.width = self.w_part_id.width_formulas + self.w_operator_selection + formula
    #         self.w_part_id.width_formulas = self.w_part_id.width


    def width_part_line(self):
        if self.w_part_id:
            formula = self.w_formula_id.name
            if self.w_formula_id.is_fixed_size:
                formula = str(self.w_formula_fixed_size)
            model_id = self.env.ref('product_configured.model_parts',raise_if_not_found=False)
            self.w_part_id.width = self.w_part_id.width_formulas + self.w_operator_selection + formula if formula else ''
            self.w_part_id.width_formulas = self.w_part_id.width_formulas + self.w_operator_selection + formula if formula else ''
            count_field = self.w_part_id.width_fields_count + 1
            c = self.w_part_id.width_fields_count
            self.w_part_id.width_fields_count = count_field
            field_str = 'x_wOperatorSelection_%s' % count_field
            print("--------------f--",field_str)
            print("--------------f--",dict(self.env['parts']._fields))
            
            arch_base = _('<?xml version="1.0"?>'
                     '<data>'
                     '<xpath expr="%s" position="%s">'
                     ) % ("//div[1][hasclass('d-flex')]", 
                     'after')
            if model_id and field_str not in dict(self.env['parts']._fields):
                c = self.w_part_id.width_fields_count = count_field
                print("--------------cc--",c)
                op_field = self.env['ir.model.fields'].sudo().create({
                    'name': 'x_wOperatorSelection_%s' % c,
                    'field_description':'cst width op',
                    'model_id':model_id.id if model_id else None,
                    'ttype':'selection',
                    'selection_ids': [
                        (0, 0, {'value': '+', 'name': '+', 'sequence': 0}),
                        (0, 0, {'value': '-', 'name': '-', 'sequence': 1}),
                        (0, 0, {'value': '*', 'name': '*', 'sequence': 1}),
                        (0, 0, {'value': '/', 'name': '/', 'sequence': 1}),
                        (0, 0, {'value': '=', 'name': '=', 'sequence': 1}),
                    ],
                })
                
#                 f = self.create_field( {'model_id':model_id,'c': c})
                formula_field = self.env['ir.model.fields'].sudo().create({
                    'name': 'x_wFormulaId_%s' %c,
                    'field_description':'cst width formula id',
                    'model_id':model_id.id if model_id else None,
                    'ttype':'many2one',
                    'relation':'formula.variable',
                })
                
                arch_base = arch_base + (
                     '<label for="%s" string=""/><div class="o_row d-flex"><field name="%s" nolabel="1" attrs="%s"/>'
                     '<field name="%s" nolabel="1" attrs="%s"/></div>'
                     ) % ( 'x_wOperatorSelection_%s' % c,'x_wOperatorSelection_%s' % c, "{'invisible': [('x_wOperatorSelection_%s' , '=', False)]}" %c, 'x_wFormulaId_%s' % c,"{'invisible': [('x_wFormulaId_%s' , '=', False)]}" %c)
            
            if self.w_formula_id.is_fixed_size:
                fixed_field_str = 'x_wFormula_Fixed_%s' % count_field
                if model_id and fixed_field_str not in dict(self.env['parts']._fields):
                    c = self.w_part_id.width_fields_count = count_field
                    fixed_size = self.env['ir.model.fields'].sudo().create({
                        'name': 'x_wFormula_Fixed_%s' % c,
                        'field_description':'cst formula fixed size',
                        'model_id':model_id.id if model_id else None,
                        'ttype':'float',
                    })
                    is_fixed_size = self.env['ir.model.fields'].sudo().create({
                        'name': 'x_Is_wFormula_Fixed_bool_%s' % c,
                        'field_description':'is cst formula fixed size',
                        'model_id':model_id.id if model_id else None,
                        'ttype':'boolean',
                    })
                    arch_base =  arch_base + ('<label for="%s" string=""/><div class="o_row d-flex"><field name="%s" nolabel="1" invisible="1"/>'
                        '<field name="%s" nolabel="1" attrs="%s"/></div>') %('x_Is_wFormula_Fixed_bool_%s'%c,'x_Is_wFormula_Fixed_bool_%s'%c,
                    'x_wFormula_Fixed_%s'%c ,"{'invisible': [('x_Is_wFormula_Fixed_bool_%s' , '=', False)]}" %c)
                    
            model_id = self.env.ref('product_configured.model_parts',raise_if_not_found=False)
            part_view = 'parts_new_width_field-%s' % self.w_part_id.width_fields_count
            View = self.env['ir.ui.view'].sudo()
            view_id = View.search([('name', '=', part_view)])
            if not view_id:
                inherit_id = self.env.ref('product_configured.pats_form_view')
                   
                arch_base = arch_base + ('</xpath>' '</data>')
                View.create({'name': 'parts_new_width_field-%s' % c,
                                             'type': 'form',
                                             'model': 'parts',
                                             'mode': 'extension',
                                             'inherit_id': inherit_id.id,
                                             'arch_base': arch_base,
                                             'active': True})
            
            if self.w_formula_id.is_fixed_size:
                self.w_part_id.write({
                    'x_wFormula_Fixed_%s' %count_field:self.w_formula_fixed_size,
                    'x_Is_wFormula_Fixed_bool_%s' %count_field:True,
                })
                check_filed = 'x_Is_wFormula_Fixed_bool_%s' %count_field
                if check_filed in dict(self.env['parts']._fields):
                    q = 'update parts set "%s"=false where "%s" is null' % ( check_filed, check_filed)
                    self.env.cr.execute(q)
            
            self.w_part_id.write({
                'x_wFormulaId_%s' %count_field:self.w_formula_id.id,
                'x_wOperatorSelection_%s' %count_field:self.w_operator_selection,
            })
            # return {
            #    'type': 'ir.actions.client',
            #    'tag': 'reload',
            # }

class PartsLengthWizard(models.TransientModel):
    _name = 'parts.length.wizard'
    _description = 'Parts Length Wizard'


    l_part_id = fields.Many2one('parts', 'Part')
    l_operator_selection = fields.Selection([('+', '+'), ('-', '-'), ('*', '*'),('/', '/'),('=', '=')], string="Operator")
    l_formula_id = fields.Many2one('formula.variable', string="Formula")
    is_l_formula_fixed_size = fields.Boolean(string='Formula Fixed Size', related="l_formula_id.is_fixed_size")
    l_formula_fixed_size = fields.Float(string="Fixed Size")
    
    # def length_part_line(self):
    #     if self.l_part_id and self.l_formula_id and self.l_operator_selection:
    #         formula = self.l_formula_id.name
    #         if self.l_formula_id.is_fixed_size:
    #             formula = str(self.l_formula_fixed_size)
    #         self.l_part_id.length = self.l_part_id.length_formulas + self.l_operator_selection + formula
    #         self.l_part_id.length_formulas = self.l_part_id.length

    def length_part_line(self):
        if self.l_part_id:
            formula = self.l_formula_id.name
            if self.l_formula_id.is_fixed_size:
                formula = str(self.l_formula_fixed_size)
            model_id = self.env.ref('product_configured.model_parts',raise_if_not_found=False)
            self.l_part_id.length = self.l_part_id.length_formulas + self.l_operator_selection + formula
            self.l_part_id.length_formulas = self.l_part_id.length_formulas + self.l_operator_selection + formula
            count_field = self.l_part_id.custom_fields_count + 1
            c = self.l_part_id.custom_fields_count
            self.l_part_id.custom_fields_count = count_field
            field_str = 'x_lOperatorSelection_%s' % count_field
            print("------------field----",field_str)
            arch_base = _('<?xml version="1.0"?>'
                         '<data>'
                         '<xpath expr="%s" position="%s">'
                         ) % ("//div[hasclass('length_size_formula')]", 
                         'after')
            if model_id and field_str not in dict(self.env['parts']._fields):
                c = self.l_part_id.custom_fields_count = count_field
                print("------------c----",c)
                op_field = self.env['ir.model.fields'].sudo().create({
                    'name': 'x_lOperatorSelection_%s' % c,
                    'field_description':'cst length op',
                    'model_id':model_id.id if model_id else None,
                    'ttype':'selection',
                    'selection_ids': [
                        (0, 0, {'value': '+', 'name': '+', 'sequence': 0}),
                        (0, 0, {'value': '-', 'name': '-', 'sequence': 1}),
                        (0, 0, {'value': '*', 'name': '*', 'sequence': 1}),
                        (0, 0, {'value': '/', 'name': '/', 'sequence': 1}),
                        (0, 0, {'value': '=', 'name': '=', 'sequence': 1}),
                    ],
                })
                formula_field = self.env['ir.model.fields'].sudo().create({
                    'name': 'x_lFormulaId_%s' %c,
                    'field_description':'cst formula id',
                    'model_id':model_id.id if model_id else None,
                    'ttype':'many2one',
                    'relation':'formula.variable',
                })
                
                arch_base = arch_base + (
                     '<label for="%s" string=""/><div class="o_row d-flex"><field name="%s" nolabel="1" attrs="%s"/>'
                     '<field name="%s" nolabel="1" attrs="%s"/></div>'
                     ) % ( 'x_lOperatorSelection_%s' % c,'x_lOperatorSelection_%s' % c, "{'invisible': [('x_lOperatorSelection_%s' , '=', False)]}" %c, 'x_lFormulaId_%s' % c,"{'invisible': [('x_lFormulaId_%s' , '=', False)]}" %c)
            
            if self.l_formula_id.is_fixed_size:
                fixed_field_str = 'x_lFormula_Fixed_%s' % count_field
                if model_id and fixed_field_str not in dict(self.env['parts']._fields):
                    c = self.l_part_id.custom_fields_count = count_field
                    fixed_size = self.env['ir.model.fields'].sudo().create({
                        'name': 'x_lFormula_Fixed_%s' % c,
                        'field_description':'cst formula fixed size',
                        'model_id':model_id.id if model_id else None,
                        'ttype':'float',
                    })
                    is_fixed_size = self.env['ir.model.fields'].sudo().create({
                        'name': 'x_Is_lFormula_Fixed_bool_%s' % c,
                        'field_description':'is cst formula fixed size',
                        'model_id':model_id.id if model_id else None,
                        'ttype':'boolean',
                    })
                    arch_base =  arch_base + ('<label for="%s" string=""/><div class="o_row d-flex"><field name="%s" nolabel="1" invisible="1"/>'
                            '<field name="%s" nolabel="1" attrs="%s"/></div>') %('x_Is_lFormula_Fixed_bool_%s'%c,'x_Is_lFormula_Fixed_bool_%s'%c,
                        'x_lFormula_Fixed_%s'%c ,"{'invisible': [('x_Is_lFormula_Fixed_bool_%s' , '=', False)]}" %c)
            
            model_id = self.env.ref('product_configured.model_parts',raise_if_not_found=False)
            part_view = 'parts_new_field-%s' % self.l_part_id.custom_fields_count
            View = self.env['ir.ui.view'].sudo()
            view_id = View.search([('name', '=', part_view)])
            if not view_id:
                inherit_id = self.env.ref('product_configured.pats_form_view')
                arch_base = arch_base + ('</xpath>' '</data>')
                View.create({'name': 'parts_new_field-%s' % c,
                                             'type': 'form',
                                             'model': 'parts',
                                             'mode': 'extension',
                                             'inherit_id': inherit_id.id,
                                             'arch_base': arch_base,
                                             'active': True})
            if self.l_formula_id.is_fixed_size:
                self.l_part_id.write({
                    'x_lFormula_Fixed_%s' %count_field: self.l_formula_fixed_size,
                    'x_Is_lFormula_Fixed_bool_%s' %count_field:True,
                })
                check_filed = 'x_Is_lFormula_Fixed_bool_%s' %count_field
                if check_filed in dict(self.env['parts']._fields):
                    q = 'update parts set "%s"=false where "%s" is null' % ( check_filed, check_filed)
                    self.env.cr.execute(q)
            self.l_part_id.write({
                'x_lFormulaId_%s' %count_field:self.l_formula_id.id,
                    'x_lOperatorSelection_%s' %count_field:self.l_operator_selection,
            })
            # return {
            #    'type': 'ir.actions.client',
            #    'tag': 'reload',
            # }
