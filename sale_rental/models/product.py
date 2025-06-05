# Copyright 2014-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2016-2021 Sodexis (http://sodexis.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Link rental service -> rented HW product
    rented_product_id = fields.Many2one(
        "product.product",
        string="Related Rented Product",
        domain=[("type", "in", ("product", "consu"))],
    )
    # Link rented HW product -> rental service
    rental_service_ids = fields.One2many(
        "product.product", "rented_product_id", string="Related Rental Services"
    )

    @api.constrains("rented_product_id", "must_have_dates", "type", "uom_id")
    def _check_rental(self):
        day_uom = self.env.ref("uom.product_uom_day")
        for product in self:
            if product.rented_product_id:
                if product.type != "service":
                    raise ValidationError(
                        _("The rental product '{}' must be of type 'Service'.").format(
                            product.name
                        )
                    )
                if not product.must_have_dates:
                    raise ValidationError(
                        _(
                            "The rental product '{}' must have the option "
                            "'Must Have Start and End Dates' checked."
                        ).format(product.name)
                    )
                # In the future, we would like to support all time UoMs
                # but it is more complex and requires additionnal developments
                if product.uom_id != day_uom:
                    raise ValidationError(
                        _(
                            "The unit of measure of the rental product '{}' must "
                            "be 'Day'."
                        ).format(product.name)
                    )

    @api.constrains("rented_product_id")
    def assign_variant_rented_product_tmpl_id(self):
        if self.env.context.get("variant_rented_product", False):
            return True
        self.mapped("product_tmpl_id").with_context(
            variant_rented_product_tmpl=True
        ).assign_rented_product_tmpl_id()


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rented_product_tmpl_id = fields.Many2one(
        "product.template",
        string="Rented Product",
    )
    rental_service_tmpl_ids = fields.One2many(
        "product.template", "rented_product_tmpl_id", string="Rental Services"
    )

    @api.constrains("product_variant_ids")
    def assign_rented_product_tmpl_id(self):
        if self.env.context.get("variant_rented_product", False):
            return True
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            rented_product_id = template.product_variant_ids.rented_product_id
            if rented_product_id:

                template.with_context(
                    rented_product_tmpl=True
                ).rented_product_tmpl_id = rented_product_id.product_tmpl_id.id
            else:
                template.with_context(
                    rented_product_tmpl=True
                ).rented_product_tmpl_id = False

        for template in self - unique_variants:
            template.with_context(
                rented_product_tmpl=True
            ).rented_product_tmpl_id = False

    @api.constrains("rented_product_tmpl_id")
    def assign_variant_rented_product_id(self):
        if self.env.context.get(
            "variant_rented_product_tmpl", False
        ) or self.env.context.get("rented_product_tmpl", False):
            return True
        for template in self:
            if len(template.product_variant_ids) == 1:
                rented_product_id = fields.first(
                    template.rented_product_tmpl_id.product_variant_ids
                )
                if rented_product_id:
                    template.product_variant_ids.with_context(
                        variant_rented_product=True
                    ).rented_product_id = rented_product_id.id
                else:
                    template.product_variant_ids.with_context(
                        variant_rented_product=True
                    ).rented_product_id = False
