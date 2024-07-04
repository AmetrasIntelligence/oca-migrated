# © 2019 ForgeFlow S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=lambda self: self._default_operating_unit(),
        readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
        index=True,
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    operating_unit_id = fields.Many2one(
        related="order_id.operating_unit_id",
        string="Operating Unit",
        store=True,
        index=True,
    )
