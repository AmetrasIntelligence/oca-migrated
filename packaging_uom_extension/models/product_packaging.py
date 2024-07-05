# Copyright 2015-2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    def _inverse_qty(self):
        """
        The inverse method is defined to make the code compatible with
        existing modules and to not break tests...
        :return:
        """
        for packaging in self:
            category_id = packaging.product_id.uom_id.category_id
            qty = packaging.qty if packaging.qty else 1.0
            uom_id = packaging.uom_id.search(
                [("factor", "=", 1.0 / qty), ("category_id", "=", category_id.id)],
                limit=1,
            )
            if not uom_id:
                uom_id = packaging.uom_id.create(
                    {
                        "name": "{} {}".format(category_id.name, qty),
                        "category_id": category_id.id,
                        "rounding": packaging.product_id.uom_id.rounding,
                        "uom_type": "bigger",
                        "factor_inv": qty,
                        "active": True,
                    }
                )
            packaging.uom_id = uom_id
