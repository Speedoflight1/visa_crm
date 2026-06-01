# visa_crm — Odoo 18 CRM for Visa Consultancies

A lightweight Odoo 18 CRM module built for visa consultancy businesses (USA visa focus, works for any country).  
Drop-in replacement for the default CRM pipeline — stripped of revenue/probability clutter and tailored for visa case tracking.

## What it adds

| Feature | Detail |
|---------|--------|
| **4-stage pipeline** | New Lead → Details Captured → Follow Up Scheduled → ID Received (won) |
| **Lead temperature** | Hot / Warm / Cold badges on every list row |
| **Visa category** | B1/B2, H1B, H4, F1, F2, J1, J2, L1, C1/D, Multiple, Other |
| **Lead type** | Individual, Agent, Individual – Multiple Profiles |
| **Application type** | Fresh Application / Refused–Reapply |
| **Service needed** | Complete Application / Just Appointment Slot / Other |
| **Follow-up date** | Dedicated date field + "Today's Follow-ups" menu under Sales |
| **Price quoted** | Float field (monetary widget, selectable column) |
| **Payment status** | None / Partial / Full |
| **WhatsApp number** | Separate field from phone; links to `wa.me` |
| **Visa checklist** | DS-160 filled, Fees submitted, Appointment booked (progress bar) |
| **Waiting for** | Approval / I-20 / Documents / Payment / Appointment / Credentials |
| **Passport & applicant fields** | Full name, DOB, Passport no/expiry, Nationality, Occupation |
| **Conversation notes** | Free-text field for call notes |
| **Travel date** | With computed "days until travel" |
| **Preferred location** | City for biometric/interview |

## Screenshots

> Pipeline (list view, grouped by stage — Details Captured / Follow-Up / ID Received start collapsed):

```
New Lead (176)        ▾  ← expanded
  Veeranna   +91 939...  B1/B2   Complete   Hot   —
  PRABHA     +91 709...  H1B     ...         Warm  Jun 2
  ...

Details Captured (1)  ▸  ← click to expand
Follow Up Scheduled   ▸
ID Received (1)       ▸
```

## Installation

### Prerequisites
- Odoo 18.0 (Community or Enterprise)
- `crm` module installed
- `crm_iap_mine` module installed (ships with Odoo 18 by default)

### Steps

1. **Download / clone** this repo into your Odoo addons path:
   ```bash
   cd /path/to/odoo/addons
   git clone https://github.com/Speedoflight1/visa_crm.git visa_crm
   ```

2. **Restart Odoo**:
   ```bash
   # Linux / Mac
   sudo systemctl restart odoo
   # Windows service
   Restart-Service odoo-server-18.0
   ```

3. **Activate developer mode** in Odoo:  
   Settings → General Settings → scroll to bottom → **Activate the developer mode**

4. **Install the module**:  
   Apps → search `visa_crm` → Install

   > If you don't see it, click **Update Apps List** first (Apps → Update Apps List).

5. Open **CRM → Sales → Pipeline** — you're done.

### Windows (Odoo installer)

If you installed Odoo via the Windows `.exe` installer, the addons path is typically:
```
C:\Program Files\Odoo 18.0.XXXXXXXX\server\odoo\addons\
```
Copy the `visa_crm` folder there, then restart the `odoo-server-18.0` Windows service.

## Customisation

All custom fields live in `models/crm_lead.py`.  
All view overrides are in `views/crm_lead_views.xml`.  
Pipeline stages are in `data/crm_stage_data.xml`.

Common tweaks:
- **Add a visa category** → edit the `visa_category` selection field in `crm_lead.py`
- **Change pipeline stages** → edit `data/crm_stage_data.xml`, then upgrade the module
- **Show/hide list columns** → use the column-picker (⚙ icon top-right of the list)

After any file change, upgrade the module:
```bash
python odoo-bin -c odoo.conf -d YOUR_DB -u visa_crm --stop-after-init
```

## Module structure

```
visa_crm/
├── __manifest__.py          # Module metadata & dependencies
├── __init__.py
├── data/
│   ├── crm_stage_data.xml   # 4 pipeline stages
│   └── crm_tag_data.xml     # (placeholder — add tags via UI)
├── models/
│   └── crm_lead.py          # All custom fields
├── security/
│   └── ir.model.access.csv  # Access rules (inherits from CRM)
└── views/
    └── crm_lead_views.xml   # Form, list, search, menu overrides
```

## Companion module: `visa_ux` (CRM Dashboard)

This repo also includes a small companion module, **`visa_ux/`**, that adds a
**CRM Dashboard** — a "Dashboard" item in the CRM top menu showing:

- Total leads, Hot leads, Follow-ups due today (clickable KPI cards)
- A "Pipeline by Stage" bar chart (click a bar to drill into that stage's list)

Built as an OWL client action (`static/src/dashboard/`), data via `read_group` — no
extra fields, no data migration.

> The module folder also contains a `manual_save.js` patch (ServiceNow-style explicit
> save) and a `notes_popover` widget (Internal Notes column with click-to-preview).
> These are **disabled in the default manifest** (kept on disk for later use). To enable
> them, add their files back to the `assets` / `data` keys in `visa_ux/__manifest__.py`.

Install it the same way as `visa_crm` (Apps → search `visa_ux` → Install). It depends on
`visa_crm`.

## Compatibility

| Odoo version | Status |
|---|---|
| 18.0 | ✅ Tested |
| 17.0 | Not tested |
| 16.0 | Not tested |

## License

LGPL-3.0 — free to use, modify, and distribute.

## Credits

Built by [eVisas](https://evisas.in) for internal use, open-sourced for the Odoo community.
