# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Sale Order Line Packaging Quantity Extension",
    "summary": "Define quantities according to product packaging on sale order lines",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Warehouse Management",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale_order_line_packaging_qty"],
    "data": ["views/product_packaging.xml"],
}
