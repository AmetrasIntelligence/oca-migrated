# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        help="Operating Unit that will be used in payments, "
        "when this journal is used.",
        index=True,
    )
