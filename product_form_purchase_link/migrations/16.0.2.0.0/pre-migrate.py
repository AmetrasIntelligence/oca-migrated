from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # The module is deprecated: Odoo's "Purchased" button replaces it, so remove
    # the views this module owned. The product form views have children in
    # ametras_product_form_purchase_link_extension, which depends on this module
    # and is updated in the same run, so it recreates them on Odoo's button.
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "product_form_purchase_link.purchase_order_line_search",
            "product_form_purchase_link.view_product_template_purchase_buttons_from",
            "product_form_purchase_link.product_normal_form_view_inherit_purchase",
        ],
        delete_childs=True,
    )
