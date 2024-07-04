# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    operating_unit_id = fields.Many2one("operating.unit", "Operating Unit", index=True)
