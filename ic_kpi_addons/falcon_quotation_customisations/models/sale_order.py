# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
from odoo.tools import pdf
import codecs


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
class SaleOrder(models.Model):
    _inherit = 'sale.order'   

    alphabets = fields.Selection([('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D'), ('5', 'E'), ('6', 'F'), ('7', 'G'), ('8', 'H'), ('9', 'I'), ('10', 'J'), ('11', 'K'), ('12', 'L'), ('13', 'M'), ('14', 'N'), ('15', 'O'), ('16', 'P'), ('17', 'Q'), ('18', 'R'), ('19', 'S'), ('20', 'T'), ('21', 'U'), ('22', 'V'), ('23', 'W'), ('24', 'X'), ('25', 'Y'), ('26', 'Z')], string='Alphabets')

    def alphabet_to_number(self, alphabet):
        if alphabet == 1:
            return 'A'
        elif alphabet == 2:
            return 'B'
        elif alphabet == 3:
            return 'C'
        elif alphabet == 4:
            return 'D'
        elif alphabet == 5:
            return 'E'
        elif alphabet == 6:
            return 'F'
        elif alphabet == 7:
            return 'G'
        elif alphabet == 8:
            return 'H'
        elif alphabet == 9:
            return 'I'
        elif alphabet == 10:
            return 'J'
        elif alphabet == 11:
            return 'K'
        elif alphabet == 12:
            return 'L'
        elif alphabet == 13:
            return 'M'
        elif alphabet == 14:
            return 'N'
        elif alphabet == 15:
            return 'O'
        elif alphabet == 16:
            return 'P'
        elif alphabet == 17:
            return 'Q'
        elif alphabet == 18:
            return 'R'
        elif alphabet == 19:
            return 'S'
        elif alphabet == 20:
            return 'T'
        elif alphabet == 21:
            return 'U'
        elif alphabet == 22:
            return 'V'
        elif alphabet == 23:
            return 'W'
        elif alphabet == 24:
            return 'X'
        elif alphabet == 25:
            return 'Y'
        elif alphabet == 26:
            return 'Z'
        else:
            return ' '

    def action_quotation_send(self):
        res = super().action_quotation_send()
        document = self.sale_order_template_id.attachment_ids
        if document:
            quotation_pdf = self.env.ref("sale.action_report_saleorder")._render_qweb_pdf(self.id)
            b64_pdf = base64.b64encode(quotation_pdf[0])
            merged_pdf = pdf.merge_pdf([quotation_pdf[0], document.raw])
            b64_pdf = base64.b64encode(merged_pdf)
            if self.state in ['draft', 'sent']:
                pdf_name = "Quotation - " + str(self.name) + ".pdf"
            else:
                pdf_name = "Order - " + str(self.name) + ".pdf"
            report_attachment = self.env["ir.attachment"].create(
                {
                    "name": pdf_name,
                    "datas": b64_pdf,
                    'res_model': 'mail.compose.message',
                    'res_id': 0,
                    "type": "binary",
                }
            )
            res['context'].update({'default_attachment_ids': [(6, 0, [report_attachment.id])]})
        else:
            quotation_pdf = self.env.ref("sale.action_report_saleorder")._render_qweb_pdf(self.id)
            b64_pdf = base64.b64encode(quotation_pdf[0])
            if self.state in ['draft', 'sent']:
                pdf_name = "Quotation - " + str(self.name) + ".pdf"
            else:
                pdf_name = "Order - " + str(self.name) + ".pdf"
            report_attachment = self.env["ir.attachment"].create(
                {
                    "name": pdf_name,
                    "datas": b64_pdf,
                    'res_model': 'mail.compose.message',
                    'res_id': 0,
                    "type": "binary",
                }
            )
            res['context'].update({'default_attachment_ids': [(6, 0, [report_attachment.id])]})
        return res

