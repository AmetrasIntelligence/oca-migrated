{
    "name": "Report Qweb PDF Fixed Column",
    "summary": """
        Fix auto-col to not change report font size caused by a
        boundary overflow""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "category": "Reporting",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/reporting-engine",
    "depends": ["web"],
    "data": [],
    "assets": {
        "web.report_assets_pdf": [
            "/report_qweb_pdf_fixed_column/static/src/css/report_qweb_pdf_fixed_column.scss",
        ],
    },
    "maintainers": ["Tardo"],
    "development_status": "Beta",
}
