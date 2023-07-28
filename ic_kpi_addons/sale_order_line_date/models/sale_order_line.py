# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 ForgeFlow S.L. (https://forgeflow.com)
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models, api, _
from datetime import date, datetime, time, timedelta
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Datetime("Delivery Date")

    @api.constrains("commitment_date")
    def _check_sale_date(self):
        for record in self:
            if record.commitment_date:
                if record.commitment_date.date() < date.today():
                    raise ValidationError(_("You Cannot Choose a Previous date"))
            
    def write(self, vals):
        # Force commitment date only if all lines are on the same sale order
        if len(self.mapped("order_id")) == 1:
            for line in self:
                if not line.commitment_date and line.order_id.commitment_date and "commitment_date" not in vals:
                    vals.update({"commitment_date": line.order_id.commitment_date})
                    break
        return super(SaleOrderLine, self).write(vals)

    def _prepare_procurement_values(self, group_id=False):
        vals = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        # has ensure_one already
        if self.commitment_date:
            vals.update({"date_deadline": self.commitment_date, "date_planned": self.commitment_date})
        return vals
