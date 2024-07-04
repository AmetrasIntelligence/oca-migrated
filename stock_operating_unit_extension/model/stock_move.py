# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    operating_unit_id = fields.Many2one(
        related="location_id.operating_unit_id",
        string="Source Location Operating Unit",
        index=True,
        store=True,
    )
    operating_unit_dest_id = fields.Many2one(
        related="location_dest_id.operating_unit_id",
        string="Dest. Location Operating Unit",
        index=True,
        store=True,
    )