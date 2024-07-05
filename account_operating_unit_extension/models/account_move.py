# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        index=True,
    )


class AccountMove(models.Model):
    _inherit = "account.move"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        default=lambda self: self._default_operating_unit_id(),
        help="This operating unit will be defaulted in the move lines.",
        readonly=True,
        states={"draft": [("readonly", False)]},
        index=True,
    )

    @api.onchange("operating_unit_id")
    def _onchange_operating_unit(self):
        if self.operating_unit_id and (
            not self.journal_id
            or self.journal_id.operating_unit_id != self.operating_unit_id
        ):
            domain = []
            if self.company_id:
                domain = [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", self.company_id.id),
                ]
            domain.append(("type", "=", self.journal_id.type))
            journal = self.env["account.journal"].search(domain)
            jf = journal.filtered(
                lambda aj: aj.operating_unit_id == self.operating_unit_id
            )
            if not jf:
                self.journal_id = journal[0]
            else:
                self.journal_id = jf[0]
            for line in self.line_ids:
                line.operating_unit_id = self.operating_unit_id
