# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    @api.model_create_multi
    def create(self, vals_list):
        records = super(OperatingUnit, self).create(vals_list)
        for rec in records:
            if self.env.user in rec.user_ids:
                rec.update({"user_ids": [fields.Command.unlink(self.env.user.id)]})
            users = (
                self.env["res.users"]
                .search([("login", "=", "__system__"), ("active", "in", [True, False])])
                .ids
            )
            if users:
                rec.update({"user_ids": [fields.Command.link(user) for user in users]})
        self.clear_caches()
        return records
