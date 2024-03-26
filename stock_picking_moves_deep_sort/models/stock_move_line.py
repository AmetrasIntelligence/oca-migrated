from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sequence = fields.Integer(default=10)

    @api.model_create_multi
    def create(self, vals):
        lines = super(StockMoveLine, self).create(vals)
        for picking_id in lines.mapped("picking_id"):
            picking_id._sort_stock_move_line()
        return lines
