from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # The module is deprecated: the active field on res.partner.bank lives in
    # Odoo core and the view adaptations are dropped, so remove the view
    # records this module owned.
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "partner_bank_active.res_partner_bank_tree_view",
            "partner_bank_active.res_partner_bank_search_view",
        ],
    )
