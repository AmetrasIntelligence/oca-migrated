# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        """
        Extends the standard Odoo create method to handle operating unit specific numbering.

        This method checks if a new sale order is being created (name='/') and
        triggers the _update_sale_order_name hook to determine the appropriate
        sequence number based on the assigned operating unit.

        :param vals: Dictionary of field values for the new sale order.
        :return: The newly created sale.order record.
        """
        if vals.get("name", "/") == "/":
            vals = self._update_sale_order_name(vals)
        return super().create(vals)

    @api.model
    def _update_sale_order_name(self, vals):
        """
        Technical hook to determine and assign the sale order name before record creation.

        If 'operating_unit_id' is present in vals, it attempts to fetch a sequence
        number via the operating unit's _get_next_sale_order_number method.
        This allows for modular extensions to override or supplement the naming
        logic (e.g., by providing separate quotation sequences).

        :param vals: Dictionary of values that will be used for record creation.
        :return: The modified (or original) vals dictionary containing the 'name'.
        """
        operating_unit_id = vals.get("operating_unit_id")
        if operating_unit_id:
            # We browse the operating unit to access its specific sequence configuration
            ou_id = self.env["operating.unit"].browse(operating_unit_id)
            # Request the next number from the operating unit's assigned sequence
            name = ou_id._get_next_sale_order_number()
            if name:
                # If a sequence number was found, we assign it to 'name' in vals
                # so it will be used during record creation.
                vals["name"] = name
        return vals
