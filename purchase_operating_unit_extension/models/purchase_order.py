# Copyright 2015-17 ForgeFlow S.L.
# - Jordi Ballester Alomar
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.addons.purchase_operating_unit.models.purchase_order import PurchaseOrder as Purchase


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        states=Purchase.READONLY_STATES,
        default=lambda self: (
            self.env["res.users"].operating_unit_default_get(self.env.uid)
        ),
        index=True,
    )

    requesting_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Requesting Operating Unit",
        states=Purchase.READONLY_STATES,
        default=lambda self: (
            self.env["res.users"].operating_unit_default_get(self.env.uid)
        ),
        index=True,
    )


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    operating_unit_id = fields.Many2one(
        related="order_id.operating_unit_id",
        string="Operating Unit",
        store=True,
        index=True,
    )
