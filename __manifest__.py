{
    'name': 'Visa CRM - eVisas',
    'version': '18.0.3.0.0',
    'category': 'Sales/CRM',
    'summary': 'Minimal CRM for Visa Consultancy',
    'description': """
Visa CRM Module for eVisas
==========================
Minimal CRM for USA visa consultancy.
- Lead status: Hot / Warm / Cold
- Visa categories: H1B, H4, B1/B2, J1, F1
- Lead types: Individual, Agent, Multi-Profile
- Follow-up scheduling with dates
- Waiting status tracking (I-20, Approval, etc.)
- Google Sheet data capture
- WhatsApp integration
    """,
    'author': 'eVisas',
    'website': 'https://evisas.odoo.com',
    'license': 'LGPL-3',
    'depends': ['crm', 'crm_iap_mine'],
    'data': [
        'security/ir.model.access.csv',
        'data/crm_stage_data.xml',
        'data/crm_tag_data.xml',
        'views/crm_lead_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
