# Copyright 2018 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    default_po_line_order = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Line Order",
        help="Select a sorting criteria for purchase order lines.",
        domain="[('model', '=', 'purchase.order.line')]",
    )
    default_po_line_order_2 = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Line Order 2",
        help="Select a second sorting criteria for purchase order lines.",
        domain="[('model', '=', 'purchase.order.line')]",
    )