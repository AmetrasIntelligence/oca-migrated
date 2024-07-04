# Copyright 2018 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    po_line_order_default = fields.Many2one(
        related="company_id.default_po_line_order",
        string="Line Order 1",
        readonly=False,
    )
    po_line_order_2_default = fields.Many2one(
        related="company_id.default_po_line_order_2",
        string="Line Order 2",
        readonly=False,
    )

    @api.onchange("po_line_order_default", "po_line_order_2_default")
    def onchange_po_line_order_default(self):
        """ Reset direction line order when user remove order field value """
        if not self.po_line_order_default and not self.po_line_order_2_default:
            self.po_line_direction_default = False