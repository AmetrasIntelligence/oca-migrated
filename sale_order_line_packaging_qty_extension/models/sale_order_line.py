# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "product_uom_qty",
        "product_uom",
        "product_packaging_id",
        "product_packaging_id.qty",
    )
    def _compute_product_packaging_qty(self):
        for sol in self:
            if (
                not sol.product_packaging_id
                or sol.product_uom_qty == 0
                or sol.product_packaging_id.qty == 0
            ):
                sol.product_packaging_qty = 0
                continue
            # Consider uom
            if sol.product_id.uom_id != sol.product_uom:
                product_qty = sol.product_uom._compute_quantity(
                    sol.product_uom_qty, sol.product_id.uom_id
                )
            else:
                product_qty = sol.product_uom_qty
            sol.product_packaging_qty = product_qty / sol.product_packaging_id.qty
