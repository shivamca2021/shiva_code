from odoo import fields, models, api, _

class Product(models.Model):
    _inherit = 'product.product'

    tax_schedule = fields.Integer(string='Tax Schedule', default=1) 
    cost_estimate_type = fields.Selection([('item_defined_cost', 'Item Defined Cost')], string='Cost Estimate Type', default='item_defined_cost')
    item_defined_cost = fields.Float(string='Item Defined Cost', default=1.0)
    is_label_size = fields.Boolean(string='Is Label Size(1 * 5)')
    sale_price_wolf = fields.Float(string='Wolf Sale Price', compute='_compute_sale_price_wolf')

    def _compute_sale_price_wolf(self):
        for each in self:
            product_pricelist = self.env['product.pricelist.item'].search([('product_id', '=', each.id), ('pricelist_id.name', 'ilike', 'Wolf')], limit=1)
            prod_tmpl_pricelist = self.env['product.pricelist.item'].search([('product_tmpl_id', '=', each.product_tmpl_id.id), ('pricelist_id.name', 'ilike', 'Wolf')], limit=1)
            if product_pricelist or prod_tmpl_pricelist:
                each.sale_price_wolf = product_pricelist.fixed_price or prod_tmpl_pricelist.fixed_price
            else:
                each.sale_price_wolf = 0.0

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(["|", "|", ("barcode", "ilike", name), ("default_code", "ilike", name), ("name", "ilike", name)] + args, limit=limit)
        if not recs:
            recs = self.search([("name", operator, name)] + args, limit=limit)
        return recs.name_get()