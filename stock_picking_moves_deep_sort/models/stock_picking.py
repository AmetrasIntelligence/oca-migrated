import logging

from natsort import natsort_keygen, ns

from odoo import api, fields, models

from .res_company import SORTING_DIRECTION
from .shared import resolve_subfields

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    line_order = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Sort Lines By",
        domain="[('model', '=', 'stock.move')]",
        default=lambda self: self.env.user.company_id.default_stock_move_order,
    )
    line_order_2 = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Sort Lines By",
        domain="[('model', '=', 'stock.move')]",
        default=lambda self: self.env.user.company_id.default_stock_move_order_2,
    )
    line_direction = fields.Selection(
        selection=SORTING_DIRECTION,
        string="Sort Direction",
        default=lambda self: self.env.user.company_id.default_stock_move_direction,
    )

    stock_move_line_order = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Sort Detailed Operations Lines By",
        domain="[('model', '=', 'stock.move.line')]",
        default=lambda self: self.env.user.company_id.default_stock_move_line_order,
    )
    stock_move_line_order_2 = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Sort Detailed Operations Lines By",
        domain="[('model', '=', 'stock.move.line')]",
        default=lambda self: self.env.user.company_id.default_stock_move_line_order_2,
    )
    stock_move_line_direction = fields.Selection(
        selection=SORTING_DIRECTION,
        string="Sort Detailed Operations Direction",
        default=lambda self: self.env.user.company_id.default_stock_move_line_direction,
    )

    @api.onchange("line_order", "line_order_2")
    def onchange_line_order(self):
        if not self.line_order and not self.line_order_2:
            self.line_direction = False

    @api.onchange("stock_move_line_order", "stock_move_line_order_2")
    def onchange_stock_move_line_order(self):
        if not self.stock_move_line_order and not self.stock_move_line_order_2:
            self.stock_move_line_direction = False

    def _sort_stock_move(self):
        if not self.line_order and not self.line_order_2 and not self.line_direction:
            return
        reverse = self.line_direction == "desc"
        sequence = 0
        try:
            sorting_key = natsort_keygen(alg=ns.REAL | ns.IGNORECASE)
            sorted_lines = self.move_ids_without_package.sorted(
                key=lambda p: (
                    sorting_key(resolve_subfields(p, self.line_order)),
                    sorting_key(resolve_subfields(p, self.line_order_2)),
                ),
                reverse=reverse,
            )
            for line in sorted_lines:
                sequence += 10
                if line.sequence == sequence:
                    continue
                line.sequence = sequence
        except Exception:
            _logger.warning("Could not sort stock picking moves!", exc_info=True)

    def _sort_stock_move_line(self):
        if (
            not self.stock_move_line_order
            and not self.stock_move_line_order_2
            and not self.stock_move_line_direction
        ):
            return
        reverse = self.stock_move_line_direction == "desc"
        move_line_sequence = 0
        try:
            sorting_key = natsort_keygen(alg=ns.REAL | ns.IGNORECASE)
            sorted_lines = self.move_line_ids_without_package.sorted(
                key=lambda p: (
                    sorting_key(resolve_subfields(p, self.stock_move_line_order)),
                    sorting_key(resolve_subfields(p, self.stock_move_line_order_2)),
                ),
                reverse=reverse,
            )
            for line in sorted_lines:
                move_line_sequence += 10
                if line.sequence == move_line_sequence:
                    continue
                line.sequence = move_line_sequence
        except Exception:
            _logger.warning("Could not sort stock picking moves lines !", exc_info=True)

    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        for record in self:
            if (
                "move_ids_without_package" in vals
                or "line_order" in vals
                or "line_order_2" in vals
                or "line_direction" in vals
            ):
                record._sort_stock_move()

            if (
                "move_line_ids_without_package" in vals
                or "stock_move_line_order" in vals
                or "stock_move_line_order_2" in vals
                or "stock_move_line_direction" in vals
            ):
                record._sort_stock_move_line()
        return res


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model_create_multi
    def create(self, vals):
        lines = super(StockMove, self).create(vals)
        for picking_id in lines.mapped("picking_id"):
            picking_id._sort_stock_move()
        return lines
