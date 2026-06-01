from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # =============================================
    # LEAD TEMPERATURE
    # =============================================
    lead_temperature = fields.Selection([
        ('hot', 'Hot'),
        ('warm', 'Warm'),
        ('cold', 'Cold'),
    ], string='Lead Status', default='warm', tracking=True)

    # =============================================
    # VISA CATEGORY
    # =============================================
    visa_category = fields.Selection([
        ('b1b2', 'B1/B2 (Visitor)'),
        ('h1b', 'H1B (Work)'),
        ('h4', 'H4 (Dependent)'),
        ('f1', 'F1 (Student)'),
        ('f2', 'F2 (Student Dependent)'),
        ('j1', 'J1 (Exchange)'),
        ('j2', 'J2 (Exchange Dependent)'),
        ('l1', 'L1 (Transfer)'),
        ('c1d', 'C1/D (Crew)'),
        ('multiple', 'Multiple'),
        ('other', 'Other'),
    ], string='Visa Category', tracking=True)

    # =============================================
    # LEAD TYPE
    # =============================================
    lead_type_visa = fields.Selection([
        ('individual', 'Individual'),
        ('agent', 'Agent'),
        ('multi_profile', 'Individual - Multiple Profiles'),
    ], string='Lead Type', default='individual', tracking=True)

    # =============================================
    # APPLICATION & SERVICE TYPE
    # =============================================
    application_type = fields.Selection([
        ('fresh', 'Fresh Application'),
        ('refused', 'Refused / Reapply'),
    ], string='Application Type', default='fresh', tracking=True)

    service_type = fields.Selection([
        ('complete', 'Complete Application'),
        ('appointment', 'Just Appointment Slot'),
        ('other', 'Other'),
    ], string='Service Needed', default='complete', tracking=True)

    # =============================================
    # VISA PROCESS CHECKLIST
    # =============================================
    has_ds160 = fields.Boolean(string='DS-160 Filled', tracking=True)
    has_fees_paid = fields.Boolean(string='Visa Fees Submitted', tracking=True)
    has_appointment = fields.Boolean(string='Appointment Booked', tracking=True)

    # =============================================
    # PRICING & PAYMENT
    # =============================================
    price_quoted = fields.Float(string='Price Quoted', tracking=True)
    payment_status = fields.Selection([
        ('none', 'No Payment'),
        ('partial', 'Partial Payment'),
        ('full', 'Full Payment'),
    ], string='Payment Status', default='none', tracking=True)

    # =============================================
    # TRAVEL & LOCATION
    # =============================================
    travel_date = fields.Date(string='Travel Date', tracking=True)
    preferred_location = fields.Char(
        string='Preferred Location',
        help='Preferred city for biometric/interview (Hyd, Mumbai, etc.)')
    num_ids = fields.Integer(
        string='No. of IDs', default=1,
        help='Number of visa profiles/applications')

    # =============================================
    # WHATSAPP
    # =============================================
    whatsapp_number = fields.Char(
        string='WhatsApp',
        help='With country code e.g. +91XXXXXXXXXX')

    # =============================================
    # FOLLOW-UP
    # =============================================
    follow_up_date = fields.Date(string='Follow-up Date', tracking=True)
    follow_up_notes = fields.Char(
        string='Follow-up Notes',
        help='e.g. call not picked, form filled, evening confirm')

    # =============================================
    # WAITING FOR
    # =============================================
    waiting_for = fields.Selection([
        ('approval', 'Approval'),
        ('i20', 'I-20 Form'),
        ('documents', 'Documents from Client'),
        ('payment', 'Payment'),
        ('appointment', 'Appointment Slot'),
        ('credentials', 'Login Credentials'),
        ('other', 'Other'),
    ], string='Waiting For', tracking=True)

    waiting_notes = fields.Char(string='Waiting Details')

    # =============================================
    # NOTES
    # =============================================
    agent_notes = fields.Text(string='Conversation')

    # =============================================
    # PROFILE COUNT (kept for backward compat)
    # =============================================
    profile_count = fields.Integer(string='No. of Profiles', default=1)

    # =============================================
    # GOOGLE SHEET FIELDS (kept for backward compat)
    # =============================================
    applicant_full_name = fields.Char(string='Full Name (from Sheet)')
    applicant_dob = fields.Date(string='Date of Birth')
    applicant_passport_no = fields.Char(string='Passport Number')
    applicant_passport_expiry = fields.Date(string='Passport Expiry')
    applicant_nationality = fields.Char(string='Nationality')
    applicant_occupation = fields.Char(string='Occupation')
    applicant_address = fields.Char(string='Address')
    sheet_submitted = fields.Boolean(string='Google Sheet Received', default=False)

    # =============================================
    # COMPUTED
    # =============================================
    days_until_travel = fields.Integer(
        string='Days to Travel',
        compute='_compute_days_until_travel', store=False)

    checklist_progress = fields.Float(
        string='Process Progress',
        compute='_compute_checklist_progress', store=False)

    @api.depends('travel_date')
    def _compute_days_until_travel(self):
        for lead in self:
            if lead.travel_date:
                delta = lead.travel_date - fields.Date.today()
                lead.days_until_travel = delta.days
            else:
                lead.days_until_travel = 0

    @api.depends('has_ds160', 'has_fees_paid', 'has_appointment')
    def _compute_checklist_progress(self):
        items = ['has_ds160', 'has_fees_paid', 'has_appointment']
        for lead in self:
            done = sum(1 for f in items if getattr(lead, f))
            lead.checklist_progress = (done / len(items)) * 100

    @api.onchange('lead_type_visa')
    def _onchange_lead_type(self):
        if self.lead_type_visa in ('agent', 'multi_profile'):
            self.priority = '2'

    def action_open_whatsapp(self):
        self.ensure_one()
        number = self.whatsapp_number or self.phone
        if number:
            clean = ''.join(c for c in number if c.isdigit() or c == '+')
            if clean.startswith('+'):
                clean = clean[1:]
            return {
                'type': 'ir.actions.act_url',
                'url': f'https://wa.me/{clean}',
                'target': 'new',
            }

    def action_visa_submit(self):
        """Explicit 'SUBMIT' button. Odoo saves the (dirty) record before any
        object-type button runs, so just clicking this persists the changes.
        We return a small toast so the user gets clear confirmation."""
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Saved',
                'message': 'Lead details submitted successfully.',
                'type': 'success',
                'sticky': False,
            },
        }

    def action_visa_schedule_call(self):
        """Open the standard 'Schedule Activity' dialog pre-set to a Call."""
        self.ensure_one()
        call_type = self.env.ref('mail.mail_activity_data_call', raise_if_not_found=False)
        ctx = dict(self.env.context)
        ctx.update({
            'default_res_model': 'crm.lead',
            'default_res_id': self.id,
        })
        if call_type:
            ctx['default_activity_type_id'] = call_type.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Schedule a Call',
            'res_model': 'mail.activity',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'target': 'new',
            'context': ctx,
        }
