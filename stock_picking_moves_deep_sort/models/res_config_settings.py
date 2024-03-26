from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    stock_move_order_default = fields.Many2one(
        related="company_id.default_stock_move_order",
        string="Line Order 1",
        readonly=False,
    )
    stock_move_order_2_default = fields.Many2one(
        related="company_id.default_stock_move_order_2",
        string="Line Order 2",
        readonly=False,
    )
    stock_move_direction_default = fields.Selection(
        related="company_id.default_stock_move_direction",
        string="Sort Direction",
        readonly=False,
    )
    stock_move_line_order_default = fields.Many2one(
        related="company_id.default_stock_move_line_order",
        string="Line Order 1",
        readonly=False,
    )
    stock_move_line_order_2_default = fields.Many2one(
        related="company_id.default_stock_move_line_order_2",
        string="Line Order 2",
        readonly=False,
    )
    stock_move_line_direction_default = fields.Selection(
        related="company_id.default_stock_move_line_direction",
        string="Sort Direction",
        readonly=False,
    )

    @api.onchange("stock_move_order_default", "stock_move_order_2_default")
    def onchange_stock_move_order_default(self):
        """Reset direction line order when user remove order field value"""
        if not self.stock_move_order_default and not self.stock_move_order_2_default:
            self.stock_move_direction_default = False

    @api.onchange("stock_move_line_order_default", "stock_move_line_order_2_default")
    def onchange_stock_move_line_order_default(self):
        """Reset direction of stock move line order
        when user remove order field value"""
        if (
            not self.stock_move_line_order_default
            and not self.stock_move_line_order_2_default
        ):
            self.stock_move_line_direction_default = False
