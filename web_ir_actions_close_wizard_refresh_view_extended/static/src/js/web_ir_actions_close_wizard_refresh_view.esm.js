/** @odoo-module **/

import {registry} from "@web/core/registry";

async function executeCloseAndRefreshView({env}) {
    const actionService = env.services.action;
    return actionService.doAction(actionService.currentController.action, {
        clearBreadcrumbs: true,
    });
}

registry
    .category("action_handlers")
    .add("ir.actions.close_wizard_refresh_view", executeCloseAndRefreshView);
