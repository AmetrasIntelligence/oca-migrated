# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    # Field Section
    origin_picking_id = fields.Many2one(
        string="Origin Picking", comodel_name="stock.picking", readonly=True
    )

    # Overloadable Section
    def _handle_orders_with_original_picking(self):
        """By default, the module cancel the original stock picking and
        set the original sale order as invoiced.
        Overload / Overwrite this function if you want another
        behaviour"""
        for order in self:
            origin_picking_id = order.origin_picking_id
            # Cancel Picking
            origin_picking_id.action_cancel()
            origin_picking_id.write({"final_pos_order_id": order.id})

            # Set Sale Order as fully invoiced
            origin_picking_id.mapped("group_id.sale_id").write(
                {
                    "invoice_status": "invoiced",
                }
            )

    # Overload Section
    @api.model
    def create_from_ui(self, orders, draft=False):
        """Cancel the original picking, when the pos order is done"""
        res = super().create_from_ui(orders, draft)
        pos_order_ids = [rec["id"] for rec in res]
        orders_with_original_picking = self.search(
            [
                ("id", "in", pos_order_ids),
                ("origin_picking_id", "!=", False),
                ("state", "!=", "draft"),
            ]
        )

        orders_with_original_picking._handle_orders_with_original_picking()

        return res

    @api.model
    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)
        if "origin_picking_id" in ui_order:
            res["origin_picking_id"] = ui_order["origin_picking_id"]
        return res

    def create_picking(self):
        """Call super() for each order separately with the origin picking id
        in the context. The new picking will be updated accordingly in the
        picking's action_confirm()"""
        for order in self:
            if order.picking_id:
                continue
            if order.origin_picking_id:
                order = order.with_context(origin_picking_id=order.origin_picking_id.id)
            super(PosOrder, order).create_picking()
        return True
