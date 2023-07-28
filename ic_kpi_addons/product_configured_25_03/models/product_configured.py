from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class ProductConfigured(models.Model):
    _name = 'product.configured'

    name = fields.Char("Cabinet Name")
    product_material_id = fields.Many2one("product.material", "Material Options")
    product_configured_line_ids = fields.One2many("product.configured.line", "product_configured_id",
                                                  string="Product Configured Items")


class ProductMaterial(models.Model):
    _name = 'product.material'

    name = fields.Char("Material Name")
    type = fields.Selection([('internal', 'Internal'), ('external', 'External')], "Type")


class StandardDimension(models.Model):
    _name = 'standard.dimension'

    name = fields.Char("Name", digits='Standard Dimension')
    width = fields.Float('Width', digits='Standard Dimension')
    height = fields.Float('Height', digits='Standard Dimension')
    depth = fields.Float('Depth', digits='Standard Dimension')
    thickness = fields.Float('Thickness', digits='Standard Dimension')
    product_template_id = fields.Many2one("product.template", "Product Template")


class ProductConfiguredLine(models.Model):
    _name = 'product.configured.line'

    
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

    name = fields.Char("Name")
    default_code = fields.Char("Internal Reference")
    responsible_id = fields.Many2one('res.users','Responsible')
    standard_price = fields.Float('Cost Price')
    qty_available = fields.Float('Quantity On Hand')
    uom_id = fields.Many2one('uom.uom','Unit of Measure')
    product_id = fields.Many2one('product.template','Product')
    part_id = fields.Many2one('product.template','Part')
    part_size = fields.Selection([('link_to_the_object', 'Link to the object'), ('fixed', 'Fixed')], 'Part Size')
    width_size = fields.Selection([('fixed_size', 'Fixed Size'), ('related_to_object', 'Related to Object')], 'Width Size')
    length_size = fields.Selection([('fixed_size', 'Fixed Size'), ('related_to_object', 'Related to Object')],
                                   'Length Size')
    width = fields.Char('Width')
    height = fields.Char('Height')
    length = fields.Char('Length')

    def configured_parts(self):
        wizard_form = self.env.ref('product_configured.product_configuration_wizard_form', False)
        return {
            'name': _('Parts Configuration'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.configuration.wizard',
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_part_id': self.id}

        }

class SubAssembly(models.Model):
    _name = 'sub.assembly'

    name = fields.Char("Name")
    default_code = fields.Char("Internal Reference")
    responsible_id = fields.Many2one('res.users','Responsible')
    standard_price = fields.Float('Cost Price')
    qty_available = fields.Float('Quantity On Hand')
    uom_id = fields.Many2one('uom.uom','Unit of Measure')
    product_id = fields.Many2one('product.template','Product')
    sub_assembly_id = fields.Many2one('product.template', 'Sub Assembly')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('width', 'height', 'depth')
    def _compute_width_height_depth(self):
        for record in self:
            width = record.width + ' x ' if record.width else '0 x '
            height = record.height + ' x ' if record.height else '0 x '
            depth = record.depth if record.depth else '0'
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
                                      ('door_hardware', 'Door Hardware'),
                                      ('hardware', 'Hardware'),
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
    width = fields.Char('Width')
    height = fields.Char('Height')
    depth = fields.Char('Depth')
    total_size = fields.Char(compute='_compute_width_height_depth', string='Width*Height*Depth', store=True)
    min_size = fields.Char(string='Min Size')
    max_size = fields.Char(string='Max Size')
    cubic_volume = fields.Char(compute='_compute_width_height_depth', string='Cubic Volume', store=True)
    route_selection = fields.Selection([('build_to_stock', 'Build To Stock'), ('build_to_job', 'Build To Job')], string='Routes')
    object_hardware_ids = fields.Many2many(
        'product.template', 'object_hardware_rel', 'product_template_id', 'object_hardware_id',
        string='Object Hardware')
    cabinet_hardware_ids = fields.Many2many(
        'product.template', 'cabinet_hardware_rel', 'product_template_id', 'cabinet_hardware_id',
        string='Cabinet Hardware')
    drawer_hardware_ids = fields.Many2many(
        'product.template', 'drawer_hardware_rel', 'product_template_id', 'drawer_hardware_id',
        string='Drawer Hardware')
    door_hardware_ids = fields.Many2many(
        'product.template', 'door_hardware_rel', 'product_template_id', 'door_hardware_id',
        string='Door Hardware')
    edge_banding_ids = fields.Many2many(
        'product.template', 'edge_banding_rel', 'product_template_id', 'edge_banding_id',
        string='Edge Banding')
    

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
