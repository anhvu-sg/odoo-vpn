{
    "name": "VPN",
    "summary": """VPN""",
    "version": "15.0.1.0.1",
    "category": "",
    "license": "AGPL-3",
    "website": "",
    "author": "",
    "sequence": 0,
    "contributors": [
    ],
    "depends": [
        "base",
        "mail",
        "queue_job",
    ],
    "data": [
        # Security
        'security/ir.model.access.csv',

        # Data
        # 'data/demo.xml',
        'data/ir_cron_data.xml',
        'data/queue_job_channel_data.xml',
        'data/queue_job_function_data.xml',
        'data/vpn_provider_data.xml',

        # Wizard

        # Views
        'views/vpn_provider.xml',
        'views/vpn_vpn.xml',

        # Views Template

        # Wizard


        # Report

        # Menu
        'menu/menu.xml'
    ],
    "demo": [
    ],
    "qweb": [
        # "static/src/xml/*.xml",
    ],
    "images": [
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": True,
    "installable": True,
}
