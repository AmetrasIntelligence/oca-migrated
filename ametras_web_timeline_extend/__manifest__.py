# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Ametras Web timeline Extend",
    "summary": "Interactive visualization chart to show events in time",
    "version": "16.0.1.0.1",
    "development_status": "Production/Stable",
    "author": "ACSONE SA/NV, "
    "Tecnativa, "
    "Monk Software, "
    "Onestein, "
    "Trobz, "
    "Odoo Community Association (OCA)",
    "category": "web",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/web",
    "depends": ["web", "web_timeline"],
    "data": [],
    "maintainers": ["tarteo"],
    "application": False,
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "ametras_web_timeline_extend/static/src/scss/web_timeline.scss",
            "ametras_web_timeline_extend/static/src/js/timeline_renderer.js",
            "ametras_web_timeline_extend/static/src/xml/web_timeline.xml",
        ],
    },
}
