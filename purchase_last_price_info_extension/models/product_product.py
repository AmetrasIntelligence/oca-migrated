# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright 2019 ForgeFlow S.L.
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends("last_purchase_line_id")
    def _compute_last_purchase_line_id_info(self):
        for item in self:
            po_line = item.sudo().last_purchase_line_id
            item.last_purchase_price = po_line.price_unit
            item.last_purchase_date = po_line.date_order
            item.last_purchase_supplier_id = po_line.partner_id
            item.last_purchase_currency_id = po_line.currency_id or item.currency_id