/* @odoo-module */
/* eslint-disable no-unused-vars */

import {XMLParser} from "@web/core/utils/xml";
import {Field} from "@web/views/fields/field";

export class CustomInfoArchParser extends XMLParser {
    parse(arch, models, modelName) {
        const archInfo = {
            fieldNames: [],
            __rawArch: arch,
            fieldNodes: {},
            activeFields: {},
        };

        this.visitXML(arch, (node) => {
            switch (node.tagName) {
                case "field":
                    this.visitField(node, archInfo, models, modelName);
                    break;
            }
        });
        return archInfo;
    }
    visitField(node, archInfo, models, modelName) {
        archInfo.fieldNames.push(node.getAttribute("name"));
        const field_name = node.getAttribute("name");
        const fields = models[modelName];
        const field = fields[field_name];
        if (field) {
            const fieldInfo = Field.parseFieldNode(node, models, modelName);
            const name = fieldInfo.name;
            archInfo.fieldNodes[name] = fieldInfo;
            for (const [key, field] of Object.entries(archInfo.fieldNodes)) {
                archInfo.activeFields[key] = field;
            }
        }
    }
}
