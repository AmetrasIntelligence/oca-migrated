{
    "name": "Stock Picking Move Deep Sort",
    "version": "16.0.1.0.0",
    "author": "Ametras intelligence, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Stock Management",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "summary": "Stock Picking Move Sort",
    "depends": ["stock"],
    "external_dependencies": {"python": ["natsort"]},
    "data": [
        "views/res_config_settings_views.xml",
        "views/stock_move_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
}
