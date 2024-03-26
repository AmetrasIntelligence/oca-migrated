from odoo import fields, models

SORTING_DIRECTION = [
    ("asc", "Ascending"),
    ("desc", "Descending"),
]


class ResCompany(models.Model):
    _inherit = "res.company"

    default_stock_move_order = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Line Order",
        help="Select a sorting criteria for stock moves.",
        domain="[('model', '=', 'stock.move')]",
    )
    default_stock_move_order_2 = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Line Order 2",
        help="Select a second sorting criteria for stock moves.",
        domain="[('model', '=', 'stock.move')]",
    )
    default_stock_move_direction = fields.Selection(
        selection=SORTING_DIRECTION,
        string="Sort Direction",
        help="Select a sorting direction for stock moves.",
    )

    default_stock_move_line_order = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Line Order",
        help="Select a sorting criteria for stock moves.",
        domain="[('model', '=', 'stock.move.line')]",
    )
    default_stock_move_line_order_2 = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Line Order 2",
        help="Select a second sorting criteria for stock moves.",
        domain="[('model', '=', 'stock.move.line')]",
    )
    default_stock_move_line_direction = fields.Selection(
        selection=SORTING_DIRECTION,
        string="Sort Direction",
        help="Select a sorting direction for stock moves.",
    )
