{
    'name': 'Visa CRM - UX Enhancements',
    'version': '18.0.1.1.0',
    'category': 'Sales/CRM',
    'summary': 'CRM dashboard for Visa CRM',
    'description': """
Visa CRM UX layer
=================
- Custom CRM dashboard (counts per stage, hot leads, follow-ups due, funnel)

Note: the manual-save patch and the internal-notes preview widget are intentionally
disabled in this build (files kept on disk for later use).
    """,
    'author': 'eVisas',
    'website': 'https://evisas.in',
    'license': 'LGPL-3',
    'depends': ['crm', 'visa_crm', 'web'],
    'data': [
        'views/dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'visa_ux/static/src/dashboard/dashboard.js',
            'visa_ux/static/src/dashboard/dashboard.xml',
            'visa_ux/static/src/scss/polish.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
