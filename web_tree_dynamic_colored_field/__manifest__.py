{
    "name": "Ametras Colorize field in tree views",
    "summary": "Allows you to dynamically color fields on tree views",
    "category": "Hidden/Dependency",
    "version": "16.0.1.0.0",
    "author": "Ametras intelligence GmbH",
    "website": "https://www.ametras.com",
    "depends": ["web"],
    "license": "OPL-1",
    "demo": ["demo/res_users.xml"],
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "/web_tree_dynamic_colored_field/static/src/js/*.js",
            "/web_tree_dynamic_colored_field/static/src/xml/*.xml",
        ],
    },
}
