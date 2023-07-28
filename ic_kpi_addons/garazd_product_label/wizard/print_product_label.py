# Copyright © 2018 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.addons.base.models.report_paperformat import PAPER_SIZES

class PrintProductLabel(models.TransientModel):
    _name = "print.product.label"
    _description = 'Product Labels Wizard'

    @api.model
    def _get_products(self):
        res = []
        if self._context.get('active_model') == 'product.template':
            products = self.env[self._context.get('active_model')].browse(self._context.get('default_product_ids'))
            for product in products:
                label = self.env['print.product.label.line'].create({
                    'product_id': product.product_variant_id.id,
                })
                res.append(label.id)
        elif self._context.get('active_model') == 'product.product':
            products = self.env[self._context.get('active_model')].browse(self._context.get('default_product_ids'))
            for product in products:
                label = self.env['print.product.label.line'].create({
                    'product_id': product.id,
                })
                res.append(label.id)
        elif self._context.get('active_model') == 'sale.order':
            sale_order = self.env[self._context.get('active_model')].browse(self._context.get('active_id'))
            for line in sale_order.order_line:
                label = self.env['print.product.label.line'].create({
                    'product_id': line.product_id.id,
                    'qty': line.product_uom_qty or 1,
                    'sale_order_id':sale_order.id
                })
                res.append(label.id)
        return res

    def _get_default_product_fields(self):
        product = self.env['ir.model'].sudo().search([('model', '=', 'product.template')])
        model_ids = self.env['ir.model.fields'].search([('model_id', '=', product.id)]).ids
        return [('id', 'in', model_ids)]

    def _get_default_paper_format(self):
        """ Gives default stage_id """
        format = self.env['report.paperformat'].sudo().search([('name', '=', 'A4 w/o header')])
        return format.id

    name = fields.Char(
        'Name',
        default='Print product labels',
    )
    message = fields.Char(
        'Message',
        readonly=True,
    )
    output = fields.Selection(
        selection=[('pdf', 'PDF')],
        string='Print to',
        default='pdf',
    )
    label_ids = fields.One2many(
        comodel_name='print.product.label.line',
        inverse_name='wizard_id',
        string='Labels for Products',
        default=_get_products,
    )
    template = fields.Selection(
        selection=[
            ('garazd_product_label.report_product_label_A4_57x35',
             'Label 57x35mm (A4: 21 pcs on a sheet, 3x7)'),
            ('garazd_product_label.report_product_label_38x25',
             'Label 38x25mm (1.5" x 1")'),
            ('garazd_product_label.report_product_label_57x32',
             'Label 57x32mm (2.25" x 1.25")'),
            ('garazd_product_label.report_product_label_196x57',
             'Label 196x57mm / 7-3/4"x2-1/4" (US Letter: 4 pcs on a sheet, 1x4)'),
            ('garazd_product_label.report_product_label_101x50',
             'Label 101x50mm / 4"x2" (US Letter: 10 pcs on a sheet, 2x5)'),
            ('garazd_product_label.report_product_label_66x25',
             'Label 66x25mm / 2-5/8"x1" (US Letter: 30 pcs on a sheet, 3x10)'),
            ('garazd_product_label.report_product_label_50x25',
             'Label 50x25mm / 2-5/8"x1" (2" x 1")'),
            ],
        string='Label template',
        default='garazd_product_label.report_product_label_A4_57x35',
    )
    qty_per_product = fields.Integer(
        string='Label quantity per product',
        default=1,
    )
    # Options
    humanreadable = fields.Boolean(
        string='Human readable barcode',
        help='Print digital code of barcode.',
        default=False,
    )
    border_width = fields.Integer(
        string='Border',
        help='Border width for labels (in pixels). Set "0" for no border.'
    )


    format = fields.Selection([(ps['key'], ps['description']) for ps in PAPER_SIZES], 'Paper size', default='A4',
                              help="Label paper Size")
    product_fields = fields.Many2many('product.fields', string='Product Label Fields')
    report_paperformat_id = fields.Many2one('report.paperformat', 'report ID', default=_get_default_paper_format)

    @api.onchange('format')
    def _onchange_label_paper_size(self):
        for record in self:
            if record.format:
                record.report_paperformat_id.format = record.format

    def action_print(self):
        """ Print labels """
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')
        if not labels:
            raise Warning(_('Nothing to print, set the quantity of labels in the table.'))
        return self.env.ref('garazd_product_label.report_product_label_A4_57x35').with_context(discard_logo_check=True).report_action(labels)

    def action_preview(self):
        """ Preview labels """
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')
        if not labels:
            raise Warning(_('Nothing to preview, set the quantity of labels in the table.'))
        return self.env.ref('%s_preview' % 'garazd_product_label.report_product_label_A4_57x35').with_context(discard_logo_check=True).report_action(labels)

    def action_set_qty(self):
        self.ensure_one()
        self.label_ids.write({'qty': self.qty_per_product})

    def action_restore_initial_qty(self):
        self.ensure_one()
        for label in self.label_ids:
            if label.qty_initial:
                label.update({'qty': label.qty_initial})
