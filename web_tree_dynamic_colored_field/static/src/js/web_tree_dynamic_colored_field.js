/** @odoo-module **/
/* py _ */

import {ListRenderer} from "@web/views/list/list_renderer";
import {patch} from "@web/core/utils/patch";

patch(ListRenderer.prototype, "web_tree_dynamic_colored_field", {
    applyColorizeHelper(record, typeAttribute, cssAttribute) {
        if (this.column.options[typeAttribute]) {
            var colors = _(this.column.options[typeAttribute].split(";"))
                .chain()
                .map(this.pairColors)
                .value()
                .filter(function CheckUndefined(value) {
                    return value !== undefined;
                });
            for (var i = 0, len = colors.length; i < len; ++i) {
                var pair = colors[i],
                    color = pair[0],
                    expression = pair[1];
                if (py.evaluate(expression, this.record.evalContext).toJSON()) {
                    return `${cssAttribute}: ${color};`;
                }
            }
        }
        return "";
    },

    /**
     * Parse `<color>: <field> <operator> <value>` forms to
     * evaluable expressions
     *
     * @param {String} pairColor `color: expression` pair
     * @returns {Array} undefined or array of color, parsed expression,
     * original expression
     */
    pairColors(pairColor) {
        if (pairColor !== "") {
            var pairList = pairColor.split(":");
            var color = pairList[0],
                // If one passes a bare color instead of an expression,
                // then we consider that color is to be shown in any case
                expression = pairList[1] ? pairList[1] : "True";
            return [color, py.parse(py.tokenize(expression)), expression];
        }
        return undefined;
    },

    getCellStyleColored(record) {
        if (
            this.column.options &&
            (this.column.options.bg_color || this.column.options.fg_color)
        ) {
            var bg_color = this.applyColorizeHelper(
                record,
                "bg_color",
                "background-color"
            );
            var fg_color = this.applyColorizeHelper(record, "fg_color", "color");
            return bg_color + fg_color;
        }
    },
});
