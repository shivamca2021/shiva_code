from odoo import models, fields, _
import logging

_logger = logging.getLogger(__name__)
import xml.etree.ElementTree as ET
import base64
from io import BytesIO

from collections import defaultdict
from pprint import pprint


class ImportOrderWizard(models.TransientModel):
    _name = 'import.order.wizard'

    file_name = fields.Binary("Upload File")

    def import_orders(self):
        def etree_to_dict(t):
            d = {t.tag: {} if t.attrib else None}
            children = list(t)
            if children:
                dd = defaultdict(list)
                for dc in map(etree_to_dict, children):
                    for k, v in dc.items():
                        dd[k].append(v)
                d = {t.tag: {k: v[0] if len(v) == 1 else v
                             for k, v in dd.items()}}
            if t.attrib:
                d[t.tag].update(('@' + k, v)
                                for k, v in t.attrib.items())
            if t.text:
                text = t.text.strip()
                if children or t.attrib:
                    if text:
                        d[t.tag]['#text'] = text
                else:
                    d[t.tag] = text
            return d
        stream = BytesIO(base64.b64decode(self.file_name))
        tree = ET.parse(stream)
        root = tree.getroot()
        values = etree_to_dict(root)
        order_id = self.env['sale.order'].sudo().browse(self.env.context.get('active_id'))
        job_number = values['Job']['Properties']['Job']['Information']['Job']['Name']
        if job_number:
            order_id.job_number = job_number.replace("'", '').replace("(", '').replace(")", '').replace(",", '')
        Rooms_list=[]
        Rooms_list.append(values['Job']['Rooms'])
        for room in Rooms_list:
            for order in room['Room']['Order']['Assemblies']['Assembly']:
                generals = []
                generals.append(order['Properties']['General'])
                for gen in generals:
                    product_id = self.env['product.product'].sudo().search(
                        [('name', '=', gen.get('Name') + ' ' + gen.get('Description'))])
                    if not product_id:
                        product_id = self.env['product.product'].sudo().create(
                            {'name': gen.get('Name') + ' ' + gen.get('Description')})
                    vals = {
                        'order_id': order_id.id,
                        'product_id': product_id.id,
                        'product_uom_qty': int(gen.get('Quantity')) if gen.get('Quantity') else 1,
                        'width': gen['Size']['Width'],
                        'height': gen['Size']['Height'],
                        'depth': gen['Size']['Depth'],
                    }
                    order_line_id = order_id.order_line.sudo().create(vals)

