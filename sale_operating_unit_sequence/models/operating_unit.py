# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    # Many2one field to hold the main sale order sequence for this operating unit.
    sale_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Sale Order Sequence",
        help="Sequence of sale order with this operating unit",
    )

    def _get_next_sale_order_number(self):
        """
        Generate a new sale order number based on the operating unit's assigned sequence.

        If a 'sale_sequence_id' is defined for this operating unit, it generates and
        returns the next number from that sequence. If no sequence is assigned,
        it returns an empty string, signaling that the standard Odoo naming logic
        (or another extension) should handle the numbering.

        :return: A string containing the next sequence number, or an empty string.
        """
        self.ensure_one()
        if self.sale_sequence_id:
            return self.sale_sequence_id.next_by_id()
        return ""
