from lxml import etree

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductConfigured(models.Model):
    _name = 'product.configured'
    _description = 'Product Configured'


    name = fields.Char("Cabinet Name")
    product_material_id = fields.Many2one("product.material", "Material Options")
    product_configured_line_ids = fields.One2many("product.configured.line", "product_configured_id",
                                                  string="Product Configured Items")


class ProductMaterial(models.Model):
    _name = 'product.material'
    _description = 'Product Material'


    name = fields.Char("Material Name")
    type = fields.Selection([('internal', 'Internal'), ('external', 'External')], "Type")


class StandardDimension(models.Model):
    _name = 'standard.dimension'
    _description = 'Standard Dimension'


    name = fields.Char("Name", digits='Standard Dimension')
    width = fields.Float('Width', digits='Standard Dimension')
    height = fields.Float('Height', digits='Standard Dimension')
    depth = fields.Float('Depth', digits='Standard Dimension')
    thickness = fields.Float('Thickness', digits='Standard Dimension')
    product_template_id = fields.Many2one("product.template", "Product Template")


class ProductConfiguredLine(models.Model):
    _name = 'product.configured.line'
    _description = 'Product Configured Line'

    
    name = fields.Char("Part")
    product_sub_id = fields.Many2one("product.template", "Product")
    product_configured_id = fields.Many2one("product.configured", "Product Configured")
    width = fields.Char("Width")
    length = fields.Char("Length ")
    thickness = fields.Char("Thickness")
    note = fields.Char("Note")
    
    product_template_id = fields.Many2one("product.template", "Product Template")

class Parts(models.Model):
    _name = 'parts'
    _description = 'Parts'

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     # OVERRIDE to add the 'available_partner_bank_ids' field dynamically inside the view.
    #     # TO BE REMOVED IN MASTER
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     l_count = 0
    #     if self.search([]):
    #         l_count = max(self.search([]).mapped('custom_fields_count'))
    #         w_count = max(self.search([]).mapped('width_fields_count'))
    #     if l_count != 0:
    #         for j in range(1,l_count+1):
    #             field_str = 'x_lOperatorSelection_%s' % j
    #             formula_field_str = 'x_lFormulaId_%s' % j

    #             if field_str in dict(self.env['parts']._fields):
    #                 part_view = 'parts_new_field-%s' % j
    #                 form_view_id = self.env['ir.ui.view'].sudo().search([('name', '=', part_view)])
    #                 if form_view_id:
    #                     # tree = etree.fromstring(res['arch'])
    #                     doc = etree.XML(res['arch'])
    #                     for node in doc.xpath("///field[@name='"+field_str+"']"):
    #                         node.set('invisible', '1')
    #                     for node in doc.xpath("///field[@name='"+formula_field_str+"']"):
    #                         node.set('invisible', '1')
    #                         res['arch'] = etree.tostring(doc, encoding='unicode') 
    #     return res

    # @api.model
    # def default_get(self, default_fields):
    #     vals = super(Parts, self).default_get(default_fields)
    #     return vals


    # def _compute_length_formula(self):
    #     for part in self:
    #         data = self.search_read([('id',  '=', part.id)])
    #         if part.l_formula_first_id and part.l_operator_selection and part.l_formula_second_id:
    #             first_formula = part.l_formula_first_id.name
    #             if part.l_formula_first_id.is_fixed_size:
    #                 first_formula = str(part.l_formula_f_fixed_size)
    #             second_formula = part.l_formula_second_id.name
    #             if part.l_formula_second_id.is_fixed_size:
    #                 second_formula = str(part.l_formula_s_fixed_size)
    #             length_formula = first_formula + str(part.l_operator_selection) + second_formula
    #             for i in data:
    #                 for j in range(1,part.custom_fields_count+1):
    #                     operation = 'x_lOperatorSelection_%s' %j
    #                     relational_data = 'x_lFormulaId_%s' %j
    #                     length_formula += i.get(operation) + i.get(relational_data)[1]
    #             part.length = length_formula

    # def _compute_width_formula(self):
    #     for part in self:
    #         data = self.search_read([('id',  '=', part.id)])
    #         if part.w_formula_first_id and part.w_operator_selection and part.w_formula_second_id:
    #             first_formula = part.w_formula_first_id.name
    #             if part.w_formula_first_id.is_fixed_size:
    #                 first_formula = str(part.w_formula_f_fixed_size)
    #             second_formula = part.w_formula_second_id.name
    #             if part.w_formula_second_id.is_fixed_size:
    #                 second_formula = str(part.w_formula_s_fixed_size)
    #             width_formula = first_formula + str(part.w_operator_selection) + second_formula
    #             for i in data:
    #                 for j in range(1,part.width_fields_count+1):
    #                     operation = 'x_wOperatorSelection_%s' %j
    #                     relational_data = 'x_wFormulaId_%s' %j
    #                     width_formula += i.get(operation) + i.get(relational_data)[1]
    #             part.width = width_formula


    name = fields.Char("Name")
    default_code = fields.Char("Internal Reference")
    responsible_id = fields.Many2one('res.users','Responsible')
    standard_price = fields.Float('Cost Price')
    qty_available = fields.Float('Quantity On Hand')
    uom_id = fields.Many2one('uom.uom','Unit of Measure')
    product_id = fields.Many2one('product.template','Product')
    part_id = fields.Many2one('product.template','Part')
    part_size = fields.Selection([('link_to_the_object', 'Link to the object'), ('fixed', 'Fixed')], 'Part Size')
    width_size = fields.Selection([('fixed_size', 'Fixed Size'), ('related_to_object', 'Related to Object')], 'Width Size', default='fixed_size')
    length_size = fields.Selection([('fixed_size', 'Fixed Size'), ('related_to_object', 'Related to Object')],
                                   'Length Size', default='fixed_size')
    width = fields.Char('Width')
    width_formulas = fields.Char(string='Width Formula')
    width_results = fields.Char('Width Results')
    width_evaluate = fields.Char('Width Evaluate')
    height = fields.Char('Height', default='Material Thickness')
    length = fields.Char('Length')
    length_formulas = fields.Char('Length Formula')
    length_results = fields.Char('Length Results')
    length_evaluate = fields.Char('Length Evaluate')

    custom_fields_count = fields.Integer(string="Custom Field Count")
    width_fields_count = fields.Integer(string="Width Field Count")

    w_formula_first_id = fields.Many2one('formula.variable', string='Formula')
    w_formula_first_fixed_size = fields.Boolean(string='Formula Fixed Size', related="w_formula_first_id.is_fixed_size")

    w_operator_selection = fields.Selection([('+', '+'), ('-', '-'), ('*', '*'),('/', '/'),('=', '=')], string="Operator")
    w_formula_second_id = fields.Many2one('formula.variable', string="Formula")
    w_formula_second_fixed_size = fields.Boolean(string='Formula Fixed Size', related="w_formula_second_id.is_fixed_size")


    w_formula_f_fixed_size = fields.Float(string="Fixed Size")
    w_formula_s_fixed_size = fields.Float(string="Fixed Size")
    l_formula_first_id = fields.Many2one('formula.variable', string='Formula')
    l_formula_first_fixed_size = fields.Boolean(string='Formula Fixed Size', related="l_formula_first_id.is_fixed_size")


    l_operator_selection = fields.Selection([('+', '+'), ('-', '-'), ('*', '*'),('/', '/'),('=', '=')], string="Operator")
    l_formula_second_id = fields.Many2one('formula.variable', string="Formula")
    l_formula_second_fixed_size = fields.Boolean(string='Formula Fixed Size', related="l_formula_second_id.is_fixed_size")

    l_formula_f_fixed_size = fields.Float(string="Fixed Size")
    l_formula_s_fixed_size = fields.Float(string="Fixed Size")

    part_formula_domain = fields.Char(string="Part Formula")


    @api.onchange('width_size')
    def onchange_width_size(self):
        self.width = ""
        self.w_formula_first_id = ""
        self.w_formula_first_fixed_size = ""
        self.w_formula_f_fixed_size = ""
        self.w_operator_selection = ""
        self.w_formula_second_id = ""
        self.w_formula_second_fixed_size = ""
        self.w_formula_s_fixed_size = ""
        self.width_formulas = ""
        self.width_evaluate = ""
        self.width_results = ""

    @api.onchange('length_size')
    def onchange_length_size(self):
        self.length = ""
        self.l_formula_first_id = ""
        self.l_formula_first_fixed_size = ""
        self.l_formula_f_fixed_size = ""
        self.l_operator_selection = ""
        self.l_formula_second_id = ""
        self.l_formula_second_fixed_size = ""
        self.l_formula_s_fixed_size = ""
        self.length_formulas = ""
        self.length_evaluate = ""
        self.length_results = ""


    @api.onchange('w_formula_first_id','w_operator_selection','w_formula_second_id' ,'w_formula_f_fixed_size', 'w_formula_s_fixed_size')
    def onchange_width_formula_changes(self):
        if self.w_formula_first_id and self.w_operator_selection and self.w_formula_second_id:
            first_formula = self.w_formula_first_id.name
            if self.w_formula_first_id.is_fixed_size:
                first_formula = str(self.w_formula_f_fixed_size)
            second_formula = self.w_formula_second_id.name
            if self.w_formula_second_id.is_fixed_size:
                second_formula = str(self.w_formula_s_fixed_size)
            self.width = first_formula + self.w_operator_selection + second_formula
            self.width_formulas = self.width
            self.width_evaluate = ""
            self.width_results = ""

    @api.onchange('l_formula_first_id','l_operator_selection','l_formula_second_id' ,'l_formula_f_fixed_size', 'l_formula_s_fixed_size')
    def onchange_length_formula_changes(self):
        if self.l_formula_first_id and self.l_operator_selection and self.l_formula_second_id:
            first_formula = self.l_formula_first_id.name
            if self.l_formula_first_id.is_fixed_size:
                first_formula = str(self.l_formula_f_fixed_size)
            second_formula = self.l_formula_second_id.name
            if self.l_formula_second_id.is_fixed_size:
                second_formula = str(self.l_formula_s_fixed_size)
            self.length = first_formula + self.l_operator_selection + second_formula
            self.length_formulas = self.length
            self.length_evaluate = ""
            self.length_results = ""

    def get_formula_variable(self, field_name, formula ,model):
        model_id = self.env['ir.model']._get('product.template').id
        field_id = self.env['ir.model.fields'].search([('model_id','=',model_id), ('name','=',field_name)], limit=1)
        if field_id.ttype in ['many2many', 'many2one', 'one2many'] and model[field_name]:
            if field_name == 'edge_banding_ids':
                formula = formula + str(model[field_name][0].width)
            if field_name == 'product_internal_material_tmpl_ids' or field_name == 'product_external_material_tmpl_ids':
                formula = formula + str(model[field_name][0].weight + model[field_name][0].thickness)
        else:
            formula = formula + '0' if field_id.ttype in ['many2many', 'many2one', 'one2many'] else formula + str(model[field_name])
        return formula

    def get_formula_variable_sale_order_line(self, field_name, formula ,model):
        model_id = self.env['ir.model']._get('sale.order.line').id
        model = self.sale_line_id
        if field_name == 'product_internal_material_tmpl_ids':
            sale_field_name = "internal_material_ids"
        elif field_name == 'product_external_material_tmpl_ids':
            sale_field_name = "external_material_ids"
        else:
            sale_field_name = field_name
        field_id = self.env['ir.model.fields'].search([('model_id','=',model_id), ('name','=',sale_field_name)], limit=1)
        if field_id.ttype in ['many2many', 'many2one', 'one2many'] and model[sale_field_name]:
            if sale_field_name == 'edge_banding_ids':
                formula = formula + str(model[sale_field_name][0].width)
            if sale_field_name == 'internal_material_ids' or sale_field_name == 'external_material_ids':
                formula = formula + str(model[sale_field_name][0].weight + model[sale_field_name][0].thickness)
        else:
            formula_field = 0.0
            if (sale_field_name == 'width') and self.sale_line_id.product_width > 0:
                formula_field = self.sale_line_id.product_width
            elif (sale_field_name == 'height') and self.sale_line_id.product_height > 0:
                formula_field = self.sale_line_id.product_height
            elif (sale_field_name == 'depth') and self.sale_line_id.product_depth > 0:
                formula_field = self.sale_line_id.product_depth
            else:
                formula_field = model[sale_field_name]
            formula = formula + '0' if field_id.ttype in ['many2many', 'many2one', 'one2many'] else formula + str(formula_field)
        return formula

    def evaluate_width(self):
        for record in self:
            new_str = ''
            formula = ''
            length = len(record.width or record.width_formulas)
            count = 0
            model = self.env['product.template'].sudo().browse(self.env.context.get('default_active_id'))
            width_formula = record.width or record.width_formulas
            for i in width_formula:
                count += 1
                if i not in ['+', '-', '*', '/', '=']:
                    new_str = new_str + i
                    if count == length:
                        try:
                            float(new_str)
                            numberic = True
                        except:
                            numberic = False
                        if numberic == False:
                            formula_variable = self.env['formula.variable'].sudo().search([('name', '=', new_str)])
                            if not formula_variable or not formula_variable.product_template_field_id:
                                raise ValidationError(
                                    _('First You have to define Product Template Field of %s formula variable') % (
                                        new_str))
                            field_name = formula_variable.product_template_field_id.name
                            if not self.env.context.get('sale_part_line_id'):
                                formula = self.get_formula_variable(field_name, formula, model)
                            else:
                                formula = self.get_formula_variable_sale_order_line(field_name, formula, model)
                        else:
                            formula = formula + new_str
                else:
                    try:
                        float(new_str)
                        numberic = True
                    except:
                        print("Not a float")
                        numberic = False
                    if numberic == False:
                        formula_variable = self.env['formula.variable'].sudo().search([('name', '=', new_str)])
                        if not formula_variable or not formula_variable.product_template_field_id:
                            raise ValidationError(
                                _('First You have to define Product Template Field of %s formula variable') % (new_str))
                        field_name = formula_variable.product_template_field_id.name
                        if not self.env.context.get('sale_part_line_id'):
                            formula = self.get_formula_variable(field_name, formula, model)
                        else:
                            formula = self.get_formula_variable_sale_order_line(field_name, formula, model)
                        formula = formula + i
                    else:
                        formula = formula + new_str + i
                    new_str = ''
            record.width_evaluate = formula
            record.width_results = eval(formula)

    def evaluate_length(self):
        for record in self:
            new_str = ''
            formula = ''
            length = len(record.length or record.length_formulas)
            count = 0
            model = self.env['product.template'].sudo().browse(self.env.context.get('default_active_id'))
            width_formula = record.length or record.length_formulas
            for i in width_formula:
                count += 1
                if i not in ['+', '-', '*', '/', '=']:
                    new_str = new_str + i
                    if count == length:
                        try:
                            float(new_str)
                            numberic = True
                        except:
                            numberic = False
                        if numberic == False:
                            formula_variable = self.env['formula.variable'].sudo().search([('name', '=', new_str)])
                            if not formula_variable or not formula_variable.product_template_field_id:
                                raise ValidationError(_('First You have to define Product Template Field of %s formula variable') % (new_str))
                            field_name = formula_variable.product_template_field_id.name
                            if not self.env.context.get('sale_part_line_id'):
                                formula = self.get_formula_variable(field_name, formula, model)
                            else:
                                formula = self.get_formula_variable_sale_order_line(field_name, formula, model)
                        else:
                            formula = formula + new_str
                else:
                    try:
                        float(new_str)
                        numberic = True
                    except:
                        numberic = False
                    if numberic == False:
                        formula_variable = self.env['formula.variable'].sudo().search([('name', '=', new_str)])
                        if not formula_variable or not formula_variable.product_template_field_id:
                            raise ValidationError(
                                _('First You have to define Product Template Field of %s formula variable') % (new_str))
                        field_name = formula_variable.product_template_field_id.name
                        if not self.env.context.get('sale_part_line_id'):
                            formula = self.get_formula_variable(field_name, formula, model)
                        else:
                            formula = self.get_formula_variable_sale_order_line(field_name, formula, model)
                        formula = formula + i
                    else:
                        formula = formula + new_str + i
                    new_str = ''
            record.length_evaluate = formula
            record.length_results = eval(formula)


    @api.model
    def create(self, vals):
        res = super(Parts, self).create(vals)
        # res.remove_last_formula()
        return res
        
    def write(self, vals):
        res = super(Parts, self).write(vals)
        # self.remove_last_formula()
        return res

    # def remove_last_formula(self):
    #     print("\n\n--------------------",self)
    #     model_id = self.env.ref('product_configured.model_parts',raise_if_not_found=False)
    #     View = self.env['ir.ui.view'].sudo()
    #     views = []
    #     part_view = 'parts_new_field-%s' % self.custom_fields_count
    #     view_id = View.search([('name', '=', part_view)])
    #     if view_id and view_id.inherit_children_ids:
    #         for i in view_id.inherit_children_ids:
    #             i.write({'active':False})
    #             operation = 'product_configured.parts_new_field-%s' % j
    #             data = view_id.inherit_children_ids.filtered(lambda x:x.xml_id==operation)
    #             views.append(data)
    #     print(views)
    #     for i in views:
    #         i.write({'active':True})
    #     # print("---------",self.custom_fields_count)
    #     # for j in range(1,self.custom_fields_count+1):
    #     #     view_id = View.search([('name', '=', part_view)])
    #     #     print("==============",view_id)
    #     #     if not view_id:
    #     #         field_str = 'x_lOperatorSelection_%s' % j
    #     #         if model_id and field_str in self.env['parts']._fields:
    #     #             inherit_id = self.env.ref('product_configured.pats_form_view')
    #     #             arch_base = _('<?xml version="1.0"?>'
    #     #                  '<xpath expr="%s" position="%s">'
    #     #                  '<field name="%s"/>'
    #     #                  '<field name="%s"/>'
    #     #                  ) % ("//button[hasclass('length_size_add_btn')]", 
    #     #                  'before', 'x_lOperatorSelection_%s' % j, 'x_lFormulaId_%s' % j)
    #                 # if self.l_formula_id.is_fixed_size:
    #                 #     arch_base =  arch_base + ('<field name="%s" invisible="1"/>'
    #                 #         '<field name="%s" attr="%s"/>') %('x_Is_lFormula_Fixed_%s'%j,
    #                 #     'x_lFormula_Fixed_%s'%j ,"{'invisible': [('x_Is_lFormula_Fixed_%s' , '=', False)]}" %j)
    #             #     arch_base = arch_base + ('</xpath>')
    #             #     aa = View.create({'name': 'parts_new_field-%s' % j,
    #             #                                  'type': 'form',
    #             #                                  'model': 'parts',
    #             #                                  'mode': 'extension',
    #             #                                  'inherit_id': inherit_id.id,
    #             #                                  'arch_base': arch_base,
    #             #                                  'active': True})
    #     return {
    #        'type': 'ir.actions.client',
    #        'tag': 'reload',
    #     }

    # @api.onchange('custom_fields_count')
    # def onchange_custom_fields_count(self):
    #     if self.custom_fields_count:
    #         ids = self.search([])
    #         for record in ids:
    #             record.write({'custom_fields_count': self.custom_fields_count})
    #         return {
    #            'type': 'ir.actions.client',
    #            'tag': 'reload',
    #         }



    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     # OVERRIDE to add the 'available_partner_bank_ids' field dynamically inside the view.
    #     # TO BE REMOVED IN MASTER
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     print("------------calll--------fields view---get calll-----ddd")
    #     if view_type == 'form':
    #         form_view_id = self.env.ref('product_configured.pats_form_view')
    #         print("----------->>>", res.get('view_id'), form_view_id)
    #         if res.get('view_id') == form_view_id.id:
    #             print("-----------",form_view_id.inherit_children_ids, range(self.custom_fields_count), self.custom_fields_count)
    #             for i in range(self.custom_fields_count):
    #                 print("-------i=====",i)
    #             # tree = etree.fromstring(res['arch'])
    #             # if len(tree.xpath("//field[contains(@name,'x_lOperatorSelection_']")) == 0:
    #             #     # Don't force people to update the account module.
    #             #     arch_tree = etree.fromstring(form_view_id.arch)
    #             #     if arch_tree.tag == 'form':
    #             #             print('----i---',i)
    #             #             arch_tree.insert(i, etree.Element('field', attrib={
    #             #                 'name': 'x_lOperatorSelection_%s' % i,
    #             #             }))
    #             #             arch_tree.insert(i, etree.Element('field', attrib={
    #             #                 'name': 'x_lFormulaId_%s' % i,
    #             #             }))
    #             #         form_view_id.sudo().write({'arch': etree.tostring(arch_tree, encoding='unicode')})
    #                 return super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     return res

class SaleParts(models.Model):
    _name = 'sale.parts'
    _inherit = ['parts']
    _description = 'Sales Parts'

    sale_line_id = fields.Many2one('sale.order.line', 'Product')
    # part_id = fields.Many2one('product.template','Part')
    # sale_part_id = fields.Many2one('product.template', 'Part')

class SubAssembly(models.Model):
    _name = 'sub.assembly'
    _description = 'Sub Assembly'
    

    name = fields.Char("Name")
    default_code = fields.Char("Internal Reference")
    responsible_id = fields.Many2one('res.users','Responsible')
    standard_price = fields.Float('Cost Price')
    qty_available = fields.Float('Quantity On Hand')
    uom_id = fields.Many2one('uom.uom','Unit of Measure')
    product_id = fields.Many2one('product.template','Product')
    sub_assembly_id = fields.Many2one('product.template', 'Sub Assembly')

class ObjectHardware(models.Model):
    _name = 'object.hardware'
    _description = 'Object Hardware'

    product_id = fields.Many2one('product.template', 'Product', domain="[('product_group', '=', 'hardware')]")
    qty = fields.Float("Quantity")

class DrawerHardware(models.Model):
    _name = 'drawer.hardware'
    _description = 'Drawer Hardware'

    product_id = fields.Many2one('product.template', 'Product', domain="[('product_group', '=', 'drawer_hardware')]")
    qty = fields.Float("Quantity")

class DoorHardware(models.Model):
    _name = 'door.hardware'
    _description = 'Door Hardware'

    product_id = fields.Many2one('product.template', 'Product', domain="[('product_group', '=', 'door_hardware')]")
    qty = fields.Float("Quantity")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('width', 'height', 'depth')
    def _compute_width_height_depth(self):
        for record in self:
            width = str(record.width) + ' x ' if record.width else '0 x '
            height = str(record.height) + ' x ' if record.height else '0 x '
            depth = str(record.depth) if record.depth else '0'
            record.total_size = width + height + depth
            if width and '/' in width:
                width_split = float(record.width.split('/')[0])
                width_split2 = float(record.width.split('/')[1])
                width = width_split/width_split2
            else:
                width=float(record.width)
            if height and '/' in height:
                height_split = float(record.height.split('/')[0])
                height_split2 = float(record.height.split('/')[1])
                height = height_split/height_split2
            else:
                height = float(record.height)
            if depth and '/' in depth:
                depth_split = float(record.depth.split('/')[0])
                depth_split2 = float(record.depth.split('/')[1])
                depth = depth_split/depth_split2
            else:
                depth = float(record.depth)
            record.cubic_volume = "{:.2f}".format(float(width) * float(height) * float(depth))


    product_material_ids = fields.Many2many("product.material", string="Product Materials")
    product_configured_line_ids = fields.One2many("product.configured.line", "product_template_id",
                                                  string="Product Configured Items")
    standard_dimension_ids = fields.One2many("standard.dimension", "product_template_id",
                                                  string="Standard Dimension")
    product_group = fields.Selection([('catelog', 'Catalog Product'),
                                     ('parts', 'Parts'),  
                                     ('sub_assembly', 'Sub Assembly'),  
                                     ('coil_stock', 'Coil Stock'),
                                      ('sheet_stock', 'Sheet Stock'),
                                     ('hardwood', 'Hardwood'),  
                                     ('accessories', 'Accessories'),
                                     ('veneer', 'Veneer'), 
                                     ('edge_banding', 'Edge Banding'),
                                      ('species', 'Species'),
                                      ('drawer_hardware', 'Drawer Hardware'),
                                      ('door_hardware', 'Door Hardware'),
                                      ('hardware', 'Hardware'),
                                      ('internal_material', 'Internal Material'),
                                      ('external_material', 'External Material'),
                                     ('miscellanies', 'Miscellanies')],
                                     required=True, default='catelog', string="Product Group")
    remove_placeholder = fields.Boolean()
    parts_line_ids = fields.One2many('parts', 'product_id', string='Parts')
    sub_assembly_line_ids = fields.One2many('sub.assembly', 'product_id', string='Sub Assembly')
    product_material_tmpl_ids = fields.Many2many(
        'product.template', 'product_material_rel', 'product_template_id', 'material_id',
        string='Material Products', domain=[('active', '=', True)])
    product_species_tmpl_ids = fields.Many2many(
        'product.template', 'product_species_rel', 'product_template_id', 'species_id',
        string='Species Products', domain=[('active', '=', True)])
    product_internal_material_tmpl_ids = fields.Many2many(
        'product.template', 'internal_product_material_rel', 'product_template_id', 'internal_material_id',
        string='Internal Material Products')
    product_external_material_tmpl_ids = fields.Many2many(
        'product.template', 'external_product_material_rel', 'product_template_id', 'external_material_id',
        string='External Material Products')
    part_ids = fields.Many2many(
        'product.template', 'product_parts_rel', 'product_template_id', 'parts_id',
        string='Parts')
    sub_assembly_ids = fields.Many2many(
        'product.template', 'product_sub_assembly_rel', 'product_template_id', 'sub_assembly_id',
        string='Sub Assembly')
    category_name = fields.Char(related='categ_id.name', store=True, string="Category Name")
    fixed_adjusted = fields.Selection([('fixed', 'Fixed'), ('adjustable', 'Adjustable')], string='Fixed/Adjustable?')
    width = fields.Float('Width')
    height = fields.Float('Height')
    depth = fields.Float('Depth')
    length = fields.Float(string="Length")
    thickness = fields.Float(string="Thikness")
    total_size = fields.Char(compute='_compute_width_height_depth', string='Width*Height*Depth', store=True)
    min_size = fields.Float(string='Min Width Size')
    max_size = fields.Float(string='Max Width Size')
    cubic_volume = fields.Char(compute='_compute_width_height_depth', string='Cubic Volume', store=True)
    route_selection = fields.Selection([('build_to_stock', 'Build To Stock'), ('build_to_job', 'Build To Job')], string='Build For?')
    object_hardware_ids = fields.Many2many(
        'product.template', 'object_hardware_rel', 'product_template_id', 'object_hardware_id',
        string='Object Hardware')
    object_hardware_line_ids = fields.One2many('object.hardware', 'product_id', string='Object Hardware')
    cabinet_hardware_ids = fields.Many2many(
        'product.template', 'cabinet_hardware_rel', 'product_template_id', 'cabinet_hardware_id',
        string='Cabinet Hardware')
    drawer_hardware_ids = fields.Many2many(
        'product.template', 'drawer_hardware_rel', 'product_template_id', 'drawer_hardware_id',
        string='Drawer Hardware')
    drawer_hardware_line_ids = fields.One2many('drawer.hardware', 'product_id', string='Drawer Hardware')
    door_hardware_ids = fields.Many2many(
        'product.template', 'door_hardware_rel', 'product_template_id', 'door_hardware_id',
        string='Door Hardware')
    door_hardware_line_ids = fields.One2many('door.hardware', 'product_id', string='Door Hardware')
    edge_banding_ids = fields.Many2many(
        'product.template', 'edge_banding_rel', 'product_template_id', 'edge_banding_id',
        string='Edge Banding')
    waste_factor = fields.Float(string='Waste Factor(%)', digits=(16, 4), default=0.0)

    def name_get(self):
        result = []
        for record in self:
            name = ''
            if record.name:
                name += str(record.name)
            if record.total_size and record.total_size != '0 x 0 x 0':
                name += ' '+ record.total_size
            result.append((record.id, name))
        return result

    # @api.model
    # def create(self, vals):
    #     res = super(ProductTemplate, self).create(vals)
    #     if vals.get('fixed_adjusted') == 'fixed' and (res.width or res.height or res.depth):
    #         for rec in res.part_ids:
    #             rec.write({'width': res.width, 'height': res.height, 'depth': res.depth})
    #     return res


    # def write(self, vals):
    #     res = super(ProductTemplate, self).write(vals)
    #     for record in self:
    #         if vals.get('fixed_adjusted') and vals.get('fixed_adjusted') == 'fixed':
    #             for part in record.part_ids:
    #                 part.write({'width': record.width, 'height': record.height, 'depth': record.depth})
    #         elif vals.get('fixed_adjusted') and vals.get('fixed_adjusted') == 'adjustable':
    #             for part in record.part_ids:
    #                 part.write({'width': False, 'height': False, 'depth': False})
    #         else:
    #             for part in record.part_ids:
    #                 part.write({'width': record.width, 'height': record.height, 'depth': record.depth})
    #     return res

    def action_add_parts(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.product_template_action")
        action['view_mode'] = 'tree,form'
        action['views'] = [(k, v) for k, v in action['views'] if v in ['tree', 'form']]
        context = {
            'add_product': self.id,
            'default_remove_placeholder': True,
            'default_sale_ok': False,
        }
        action['context'] = context
        action['domain'] = [('product_group', '=', 'parts')]
        return action

    def action_add_sub_assembly(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.product_template_action")
        tree_view = [(self.env.ref('product.product_template_tree_view').id, 'tree')]
        action['view_mode'] = 'tree,form'
        action['views'] = [(k, v) for k, v in action['views'] if v in ['tree', 'form']]
        context = {
            'add_sub_assembly': self.id,
            'default_remove_placeholder': True,
        }
        action['domain'] = ['|', ('sale_ok', '=', True), ('purchase_ok', '=', True), ('type', '!=', 'service'),
                            ('remove_placeholder', '=', False)]
        action['context'] = context
        return action

    def add_parts_product(self):
        if self.env.context.get('add_product'):
            part_ids = self.browse(self.env.context.get('active_ids'))
            product_templ_id = self.env['product.template'].sudo().browse(self.env.context.get('add_product'))
            for rec in part_ids:
                vals = {'name': rec.name,
                        'default_code': rec.default_code,
                        'responsible_id': rec.responsible_id.id,
                        'standard_price': rec.standard_price,
                        'qty_available': rec.qty_available,
                        'uom_id': rec.uom_id.id,
                        'part_id': rec.id,
                        'product_id': product_templ_id.id
                        }

                part_id = self.env['parts'].sudo().create(vals)
            action = self.env["ir.actions.actions"]._for_xml_id("sale.product_template_action")
            form_view = [(self.env.ref('product.product_template_only_form_view').id, 'form')]
            action['views'] = form_view
            action['res_id'] = product_templ_id.id
            return action
        elif self.env.context.get('add_sub_assembly'):
            sub_assembly_ids = self.browse(self.env.context.get('active_ids'))
            product_templ_id = self.env['product.template'].sudo().browse(self.env.context.get('add_sub_assembly'))
            for rec in sub_assembly_ids:
                vals = {'name': rec.name,
                        'default_code': rec.default_code,
                        'responsible_id': rec.responsible_id.id,
                        'standard_price': rec.standard_price,
                        'qty_available': rec.qty_available,
                        'uom_id': rec.uom_id.id,
                        'sub_assembly_id': rec.id,
                        'product_id': product_templ_id.id
                        }
                assembly_id = self.env['sub.assembly'].sudo().create(vals)
            action = self.env["ir.actions.actions"]._for_xml_id("sale.product_template_action")
            form_view = [(self.env.ref('product.product_template_only_form_view').id, 'form')]
            action['views'] = form_view
            action['res_id'] = product_templ_id.id
            return action
        elif self.env.context.get('default_product_group') == 'parts':
            wizard_form = self.env.ref('product_configured.parts_add_product_wizard', False)
            return {
                'name': _('Add Parts to product'),
                'type': 'ir.actions.act_window',
                'res_model': 'parts.add.wizard',
                'view_id': wizard_form.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new'
            }
        else:
            raise ValidationError(_('This Button will only used from product'))

    def set_internal_material_attribute(self, res, mode):
        prod_attr_val_obj = self.env['product.attribute.value']
        internal_material_attr_id = self.env.ref('product_configured.product_attribute_internal_material')
        internal_material_ids = []

        # To create internal material variant
        if mode == 'create':
            for internal_product in res.product_internal_material_tmpl_ids:
                prod_attr_val_rec = prod_attr_val_obj.search(
                    [('name', '=', internal_product.name), (['attribute_id', '=', internal_material_attr_id.id])], limit=1)
                if prod_attr_val_rec:
                    attr_val = prod_attr_val_rec
                else:
                    attr_val = prod_attr_val_obj.create({
                        'name': internal_product.name,
                        'attribute_id': internal_material_attr_id.id
                    })
                internal_material_ids.append(attr_val.id)
        if mode == 'write':
            prod_attr_val_rec = prod_attr_val_obj.search(
                [('name', '=', res.name), (['attribute_id', '=', internal_material_attr_id.id])], limit=1)
            if prod_attr_val_rec:
                attr_val = prod_attr_val_rec
            else:
                attr_val = prod_attr_val_obj.create({
                    'name': res.name,
                    'attribute_id': internal_material_attr_id.id
                })
            internal_material_ids.append(attr_val.id)
        return internal_material_ids

    def set_external_material_attribute(self, res, mode):
        prod_attr_val_obj = self.env['product.attribute.value']
        external_material_attr_id = self.env.ref('product_configured.product_attribute_external_material')
        external_material_ids = []

        # To create external material variant
        if mode == 'create':
            for external_product in res.product_external_material_tmpl_ids:
                prod_attr_val_rec = prod_attr_val_obj.search(
                    [('name', '=', external_product.name), (['attribute_id', '=', external_material_attr_id.id])], limit=1)
                if prod_attr_val_rec:
                    attr_val = prod_attr_val_rec
                else:
                    attr_val = prod_attr_val_obj.create({
                        'name': external_product.name,
                        'attribute_id': external_material_attr_id.id
                    })
                external_material_ids.append(attr_val.id)
        if mode == 'write':
            prod_attr_val_rec = prod_attr_val_obj.search(
                [('name', '=', res.name), (['attribute_id', '=', external_material_attr_id.id])], limit=1)
            if prod_attr_val_rec:
                attr_val = prod_attr_val_rec
            else:
                attr_val = prod_attr_val_obj.create({
                    'name': res.name,
                    'attribute_id': external_material_attr_id.id
                })
            external_material_ids.append(attr_val.id)
        return external_material_ids

    def create_attribute_line(self, attribute_id, value_ids, product_tmpl_id, mode, line):
        prod_tmpl_attr_line = self.env['product.template.attribute.line']
        if mode == 'create':
            prod_tmpl_attr_line.create({'attribute_id': attribute_id,
                                    'value_ids': [(6, 0, value_ids)],
                                    'product_tmpl_id': product_tmpl_id})
        else:
            line.value_ids = [(4, value_ids)]
        return True

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        return super(ProductTemplate, self.with_context(product_copy=True)).copy(default)

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        prod_attr_val_obj = self.env['product.attribute.value']

        if self._context.get('product_copy', False) == False:
            if res.product_internal_material_tmpl_ids:
                internal_material_attr_id = self.env.ref('product_configured.product_attribute_internal_material')
                internal_material_ids = self.set_internal_material_attribute(res, 'create')

                self.create_attribute_line(internal_material_attr_id.id, internal_material_ids, res.id, 'create', False)

            if res.product_external_material_tmpl_ids:
                external_material_attr_id = self.env.ref('product_configured.product_attribute_external_material')
                external_material_ids = []

                # To create external material variant
                for external_product in res.product_external_material_tmpl_ids:
                    prod_attr_val_rec = prod_attr_val_obj.search(
                        [('name', '=', external_product.name), (['attribute_id', '=', external_material_attr_id.id])],
                        limit=1)
                    if prod_attr_val_rec:
                        attr_val = prod_attr_val_rec
                    else:
                        attr_val = prod_attr_val_obj.create({
                            'name': external_product.name,
                            'attribute_id': external_material_attr_id.id
                        })
                    external_material_ids.append(attr_val.id)
                self.create_attribute_line(external_material_attr_id.id, external_material_ids, res.id, 'create', False)

        if self.env.context.get('is_part'):
            res.product_group='parts'
        if self.env.context.get('is_subassembly'):
            res.product_group='sub_assembly'
        if self.env.context.get('is_edgebanding'):
            res.product_group='edge_banding'
        if self.env.context.get('is_species'):
            res.product_group='species'
        if self.env.context.get('is_hardware'):
            res.product_group='hardware'
        if self.env.context.get('is_drawerhardware'):
            res.product_group='drawer_hardware'
        if self.env.context.get('is_doorhardware'):
            res.product_group='door_hardware'
        if self.env.context.get('is_internal_material'):
            res.product_group='internal_material'
        if self.env.context.get('is_external_material'):
            res.product_group='external_material'
        return res

    def write(self, vals):
        prod_attr_val_obj = self.env['product.attribute.value']
        if vals.get('product_internal_material_tmpl_ids'):
            internal_material_attr_id = self.env.ref('product_configured.product_attribute_internal_material')
            internal_material_ids = []
            if self.product_internal_material_tmpl_ids:
                to_create_int_mat = set(vals.get('product_internal_material_tmpl_ids')[0][2]) - set(self.product_internal_material_tmpl_ids.ids)
                to_remove_int_mat = set(
                    self.product_internal_material_tmpl_ids.ids) - set(vals.get('product_internal_material_tmpl_ids')[0][2])

                if list(to_create_int_mat):
                    flag = 0
                    for i in list(to_create_int_mat):
                        attr_prod = self.browse(i)
                        int_mat_id = self.set_internal_material_attribute(attr_prod, 'write')
                        internal_material_ids.append(int_mat_id[0])
                        if self.attribute_line_ids:
                            line_attr = []
                            for line in self.attribute_line_ids:
                                line_attr.append(line.attribute_id)
                            if internal_material_attr_id in line_attr:
                                flag = 0
                                for line in self.attribute_line_ids:
                                    if line.attribute_id == internal_material_attr_id:
                                        self.create_attribute_line(False, int_mat_id[0], False, 'write', line)
                                        line.value_ids = [(4, int_mat_id[0])]
                            else:
                                flag = 1
                        else:
                            flag = 1
                    if flag == 1:
                        self.create_attribute_line(internal_material_attr_id.id, internal_material_ids, self.id,
                                                   'create')

                if list(to_remove_int_mat):
                    for i in list(to_remove_int_mat):
                        attr_prod = self.browse(i)
                        prod_attr_val_rec = prod_attr_val_obj.search(
                            [('name', '=', attr_prod.name), (['attribute_id', '=', internal_material_attr_id.id])], limit=1)
                        if prod_attr_val_rec:
                            for line in self.attribute_line_ids:
                                if line.attribute_id == internal_material_attr_id:
                                    line.value_ids = [(3, prod_attr_val_rec.id, _)]

            else:
                for i in vals.get('product_internal_material_tmpl_ids')[0][2]:
                    attr_prod = self.browse(i)
                    int_mat_id = self.set_internal_material_attribute(attr_prod, 'write')
                    internal_material_ids.append(int_mat_id[0])

                self.create_attribute_line(internal_material_attr_id.id, internal_material_ids, self.id, 'create', False)
        if vals.get('product_external_material_tmpl_ids'):
            external_material_attr_id = self.env.ref('product_configured.product_attribute_external_material')
            external_material_ids = []
            if self.product_external_material_tmpl_ids:
                to_create_ext_mat = set(vals.get('product_external_material_tmpl_ids')[0][2]) - set(self.product_external_material_tmpl_ids.ids)
                to_remove_ext_mat = set(
                    self.product_external_material_tmpl_ids.ids) - set(vals.get('product_external_material_tmpl_ids')[0][2])

                if list(to_create_ext_mat):
                    flag = 0
                    for i in list(to_create_ext_mat):
                        attr_prod = self.browse(i)
                        ext_mat_id = self.set_external_material_attribute(attr_prod, 'write')
                        external_material_ids.append(ext_mat_id[0])
                        if self.attribute_line_ids:
                            line_attr = []
                            for line in self.attribute_line_ids:
                                line_attr.append(line.attribute_id)
                            if external_material_attr_id in line_attr:
                                flag = 0
                                for line in self.attribute_line_ids:
                                    if line.attribute_id == external_material_attr_id:
                                        self.create_attribute_line(False, ext_mat_id[0], False, 'write', line)
                                        line.value_ids = [(4, ext_mat_id[0])]
                            else:
                                flag = 1
                        else:
                            flag = 1
                    if flag == 1:
                        self.create_attribute_line(external_material_attr_id.id, external_material_ids, self.id,
                                                   'create')

                if list(to_remove_ext_mat):
                    for i in list(to_remove_ext_mat):
                        attr_prod = self.browse(i)
                        prod_attr_val_rec = prod_attr_val_obj.search(
                            [('name', '=', attr_prod.name), (['attribute_id', '=', external_material_attr_id.id])], limit=1)
                        if prod_attr_val_rec:
                            for line in self.attribute_line_ids:
                                if line.attribute_id == external_material_attr_id:
                                    line.value_ids = [(3, prod_attr_val_rec.id, _)]
            else:
                for i in vals.get('product_external_material_tmpl_ids')[0][2]:
                    attr_prod = self.browse(i)
                    ext_mat_id = self.set_external_material_attribute(attr_prod, 'write')
                    external_material_ids.append(ext_mat_id[0])

                self.create_attribute_line(external_material_attr_id.id, external_material_ids, self.id, 'create', False)
        return super(ProductTemplate, self).write(vals)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # def add_parts_product(self):
    #     if self.env.context.get('add_product'):
    #         part_ids = self.browse(self.env.context.get('active_ids'))
    #         product_templ_id = self.env['product.template'].sudo().browse(self.env.context.get('add_product'))
    #         for rec in part_ids:
    #             vals = {'name': rec.name,
    #                     'default_code': rec.default_code,
    #                     'responsible_id': rec.responsible_id.id,
    #                     'standard_price': rec.standard_price,
    #                     'qty_available': rec.qty_available,
    #                     'uom_id': rec.uom_id.id,
    #                     'part_id': rec.id,
    #                     'product_id': product_templ_id.id
    #                     }
    #
    #             part_id = self.env['parts'].sudo().create(vals)
    #         action = self.env["ir.actions.actions"]._for_xml_id("sale.product_template_action")
    #         form_view = [(self.env.ref('product.product_template_only_form_view').id, 'form')]
    #         action['views'] = form_view
    #         action['res_id'] = product_templ_id.id
    #         return action
    #     elif self.env.context.get('add_sub_assembly'):
    #         sub_assembly_ids = self.browse(self.env.context.get('active_ids'))
    #         product_templ_id = self.env['product.template'].sudo().browse(self.env.context.get('add_sub_assembly'))
    #         for rec in sub_assembly_ids:
    #             vals = {'name': rec.name,
    #                     'default_code': rec.default_code,
    #                     'responsible_id': rec.responsible_id.id,
    #                     'standard_price': rec.standard_price,
    #                     'qty_available': rec.qty_available,
    #                     'uom_id': rec.uom_id.id,
    #                     'sub_assembly_id': rec.id,
    #                     'product_id': product_templ_id.id
    #                     }
    #             assembly_id = self.env['sub.assembly'].sudo().create(vals)
    #         action = self.env["ir.actions.actions"]._for_xml_id("sale.product_template_action")
    #         form_view = [(self.env.ref('product.product_template_only_form_view').id, 'form')]
    #         action['views'] = form_view
    #         action['res_id'] = product_templ_id.id
    #         return action
    #     elif self.env.context.get('default_product_group') == 'parts':
    #         wizard_form = self.env.ref('product_configured.parts_add_product_wizard', False)
    #         return {
    #             'name': _('Add Parts to product'),
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'parts.add.wizard',
    #             'view_id': wizard_form.id,
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'target': 'new'
    #         }
    #     else:
    #         raise ValidationError(_('This Button will only used from product'))
