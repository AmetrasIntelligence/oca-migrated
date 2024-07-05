# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_id",
        store=True,
        index=True,
    )
