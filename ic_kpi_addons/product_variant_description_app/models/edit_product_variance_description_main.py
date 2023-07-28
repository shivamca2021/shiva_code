# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang, get_lang

class ProductInherit(models.Model):
	_inherit = "product.product"

	description_for_sale = fields.Text()
	description_for_vendor = fields.Text()
	description_for_delivery = fields.Text()
	description_for_receipt = fields.Text()


class ProductTemplateInherit(models.Model):
	_inherit = "product.template"

	description_delivery = fields.Text()
	description_receipt = fields.Text()

class InheirtSaleOrder(models.Model):
	_inherit = "sale.order"

class InheritSaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	@api.onchange('product_id','product_uom_qty')
	def product_id_change(self):
		if not self.product_id:
			return
		valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
		# remove the is_custom values that don't belong to this template
		for pacv in self.product_custom_attribute_value_ids:
			if pacv.custom_product_template_attribute_value_id not in valid_values:
				self.product_custom_attribute_value_ids -= pacv

		# remove the no_variant attributes that don't belong to this template
		for ptav in self.product_no_variant_attribute_value_ids:
			if ptav._origin not in valid_values:
				self.product_no_variant_attribute_value_ids -= ptav

		vals = {}
		if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
			vals['product_uom'] = self.product_id.uom_id
			vals['product_uom_qty'] = self.product_uom_qty or 1.0

		product = self.product_id.with_context(
			lang=get_lang(self.env, self.order_id.partner_id.lang).code,
			partner=self.order_id.partner_id,
			quantity=vals.get('product_uom_qty') or self.product_uom_qty,
			date=self.order_id.date_order,
			pricelist=self.order_id.pricelist_id.id,
			uom=self.product_uom.id
		)

		vals.update(name=self.get_sale_order_line_multiline_description_sale(product))
		bom_ids = self.env["mrp.bom"].search([("product_tmpl_id","=",self.product_template_id.id)])
		description = product.description_for_sale
		if description:
			main_description = vals.get('name') + '\n' + description
			vals.update({'name': main_description})
		self._compute_tax_id()
		if bom_ids:
			bom_dict={self.product_id.description_sale:"\n	"}
			for bom_id in bom_ids:
				for line in bom_id.bom_line_ids:
					bom_dict.update({line.product_id.name:line.product_qty * self.product_uom_qty})
			bom_desc = '\n'.join("{}: {}".format(k, v) for k, v in bom_dict.items())
			vals.update({'name': bom_desc})

		if self.order_id.pricelist_id and self.order_id.partner_id:
			vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
		self.update(vals)

		title = False
		message = False
		result = {}
		warning = {}
		if product.sale_line_warn != 'no-message':
			title = _("Warning for %s", product.name)
			message = product.sale_line_warn_msg
			warning['title'] = title
			warning['message'] = message
			result = {'warning': warning}
			if product.sale_line_warn == 'block':
				self.product_id = False

		return result


	def _prepare_procurement_values(self, group_id=False):
		res = super(InheritSaleOrderLine, self)._prepare_procurement_values(group_id)
		product_id = self.env["product.product"].browse(self.product_id.id)
		res.update({'delivery_description':product_id.description_for_delivery or product_id.description_delivery})
		return res

class StockRuleInherit(models.Model):
	_inherit = 'stock.rule'

	def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
		res = super(StockRuleInherit, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
		res['desc'] = product_id.description_for_delivery or product_id.description_delivery
		return res

class InheritStockMove(models.Model):
	_inherit = "stock.move"

	desc = fields.Char("Description")

class InheritStockPicking(models.Model):
	_inherit = "stock.picking"

	desc = fields.Char("Description")

	@api.onchange('move_ids_without_package')
	def onchange_description(self):
		
		for line in self.move_ids_without_package:
			variant_id = self.env["product.product"].browse(line.product_id.id)

			if self.picking_type_id.name == "Delivery Orders":
				description = variant_id.description_for_delivery or variant_id.description_delivery
			elif self.picking_type_id.name == "Receipts":
				description = variant_id.description_for_receipt or variant_id.description_receipt

			line.desc = description

class InheritPurchaseOrder(models.Model):
	_inherit = "purchase.order.line"

	receipt_description = fields.Text("Description for Receipts")

	def _product_id_change(self):
		if not self.product_id:
			return

		self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
		product_lang = self.product_id.with_context(
			lang=get_lang(self.env, self.partner_id.lang).code,
			partner_id=self.partner_id.id,
			company_id=self.company_id.id,
		)
		self.name = self._get_product_purchase_description(product_lang)
		description = self.product_id.description_for_vendor
		if description:
			self.name += '\n' + description
		self._compute_tax_id()


	def _prepare_stock_moves(self, picking):
		res = super(InheritPurchaseOrder, self)._prepare_stock_moves(picking)
		product_id = self.env["product.product"].browse(self.product_id.id)
		if res:
			res[0].update({'desc':product_id.description_for_receipt or product_id.description_receipt})
		return res