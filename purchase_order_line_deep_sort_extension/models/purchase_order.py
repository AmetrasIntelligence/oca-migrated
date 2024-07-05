# Copyright 2018 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# Copyright 2019 Tecnativa - Pedro M. Baeza
# Copyright 2019 Tecnativa - Sergio Teruel
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

import logging

from odoo import api, fields, models

from odoo.addons.purchase_order_line_deep_sort.models.purchase_order import (
    PurchaseOrder as Purchase,
)

_logger = logging.getLogger(__name__)

string_types = ["char", "text", "date", "datetime", "selection"]


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    line_order = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Sort Lines By",
        domain="[('model', '=', 'purchase.order.line')]",
        default=lambda self: self.env.user.company_id.default_po_line_order,
    )
    line_order_2 = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Sort Lines By",
        domain="[('model', '=', 'purchase.order.line')]",
        default=lambda self: self.env.user.company_id.default_po_line_order_2,
    )

    @api.onchange("line_order", "line_order_2")
    def onchange_line_order(self):
        if not self.line_order and not self.line_order_2:
            self.line_direction = False

    def _sort_purchase_line(self):
        def resolve_subfields(obj, line_order):
            if not line_order:
                return None
            val = getattr(obj, line_order.name)
            # Odoo object
            if isinstance(val, models.BaseModel):
                if not val:
                    val = ""
                elif hasattr(val[0], "name"):
                    val = ",".join(val.mapped("name"))
                else:
                    val = ",".join([str(id) for id in val.mapped("id")])
            elif line_order.ttype in string_types:
                if not val:
                    val = ""
                elif not isinstance(val, str):
                    try:
                        val = str(val)
                    except Exception:
                        val = ""
            return val

        if (
            not self.line_order and not self.line_order_2 and not self.line_direction
        ) or self.order_line.filtered(lambda p: p.display_type == "line_section"):
            return
        reverse = self.line_direction == "desc"
        sequence = 0
        try:
            sorted_lines = self.order_line.sorted(
                key=lambda p: (
                    p.display_type is False,
                    resolve_subfields(p, self.line_order),
                    resolve_subfields(p, self.line_order_2),
                ),
                reverse=reverse,
            )
            for line in sorted_lines:
                sequence += 10
                if line.sequence == sequence:
                    continue
                line.sequence = sequence
        except Exception:
            _logger.warning("Could not sort purchase order!", exc_info=True)

    def write(self, values):
        res = super(Purchase, self).write(values)
        if (
            "order_line" in values
            or "line_order" in values
            or "line_order_2" in values
            or "line_direction" in values
        ):
            for record in self:
                record._sort_purchase_line()
        return res
