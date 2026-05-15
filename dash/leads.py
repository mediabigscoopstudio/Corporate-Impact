from django.db import models
from django.utils import timezone

from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# ─────────────────────────────────────────────
# SHARED STATUS CHOICES  (used by both models)
# ─────────────────────────────────────────────
class LeadStatus(models.TextChoices):
    NEW        = 'new',        'New'
    CONTACTED  = 'contacted',  'Contacted'
    REVIEWING  = 'reviewing',  'Reviewing'
    APPROVED   = 'approved',   'Approved'
    REJECTED   = 'rejected',   'Rejected'
    PUBLISHED  = 'published',  'Published'


# ─────────────────────────────────────────────
# 1.  HOMEMAKER LEAD
# ─────────────────────────────────────────────
class HomemakerLead(models.Model):

    class SpotlightType(models.TextChoices):
        STORY       = 'story',       'Share My Story'
        INTERVIEW   = 'interview',   'Request an Interview'
        OF_THE_MONTH = 'otm',        'Homemaker of the Month'
        WRITE       = 'write',       'Write for the Column'

    # ── Contact details ──────────────────────
    name    = models.CharField(max_length=100, verbose_name='Full Name')
    email   = models.EmailField(unique=False, verbose_name='Email Address')
    phone   = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Phone Number',
        help_text='Optional — include country code e.g. +91 98765 43210',
    )
    city    = models.CharField(max_length=100, verbose_name='City')

    # ── Story details ─────────────────────────
    story_summary = models.TextField(
        verbose_name='Your Story',
        help_text='Tell us about yourself — your journey, what you manage, and what makes your story worth telling.',
    )
    years_as_homemaker = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Years as a Homemaker',
    )

    # ── Entrepreneurship ──────────────────────
    is_entrepreneur = models.BooleanField(
        default=False,
        verbose_name='Running a Business or Side Venture?',
        help_text='Tick if you run any kind of business, home enterprise, or side venture.',
    )
    business_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Business / Venture Name',
        help_text='Leave blank if not applicable.',
    )

    # ── Social presence ───────────────────────
    instagram_handle = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Instagram Handle',
        help_text='@handle — optional but helpful for amplification.',
    )

    # ── What they want ────────────────────────
    spotlight_type = models.CharField(
        max_length=20,
        choices=SpotlightType.choices,
        default=SpotlightType.STORY,
        verbose_name='How Would You Like to Be Featured?',
    )

    # ── Consent ───────────────────────────────
    consent_publish = models.BooleanField(
        default=False,
        verbose_name='Consent to Publish',
        help_text='I agree that Corporate Impact may publish my story across print, digital, and social media.',
    )

    # ── Admin / workflow ──────────────────────
    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        verbose_name='Lead Status',
    )
    internal_notes = models.TextField(
        blank=True,
        verbose_name='Internal Notes',
        help_text='Editorial team use only — not visible to the applicant.',
    )

    # ── Timestamps ────────────────────────────
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Submitted At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    class Meta:
        verbose_name        = 'Homemaker Lead'
        verbose_name_plural = 'Homemaker Leads'
        ordering            = ['-created_at']
        indexes             = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['spotlight_type']),
        ]

    def __str__(self):
        return f'{self.name} — {self.get_spotlight_type_display()} ({self.get_status_display()})'

    @property
    def is_new(self):
        return self.status == LeadStatus.NEW

    @property
    def is_approved(self):
        return self.status == LeadStatus.APPROVED

    # ── Custom File Size Validator ─────────────────
def validate_file_size(value):
    limit = 5 * 1024 * 1024 # 5 MB in bytes
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MB.')

# ─────────────────────────────────────────────
# 2.  BYLINE LEAD
# ─────────────────────────────────────────────
class BylineLead(models.Model):

    class Tier(models.TextChoices):
        GUEST_OPED  = 'op_ed',     'Guest Op-Ed (Free)'
        COLUMNIST   = 'columnist', 'Resident Columnist (Pro)'
        BRAND_COLLAB = 'brand',    'Brand Collab (Enterprise)'

    # ── Contact details ───────────────────────
    name  = models.CharField(max_length=100, verbose_name='Full Name')
    email = models.EmailField(unique=False, verbose_name='Work Email Address')
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Phone Number',
        help_text='Optional.',
    )
    city  = models.CharField(max_length=100, verbose_name='City')

    # ── Professional identity ─────────────────
    organisation = models.CharField(
        max_length=200,
        verbose_name='Organisation / Company',
        help_text='Company, institution, or "Independent" if freelancing.',
    )
    designation = models.CharField(
        max_length=200,
        verbose_name='Designation / Title',
    )

    # ── Program interest ──────────────────────
    tier = models.CharField(
        max_length=20,
        choices=Tier.choices,
        default=Tier.GUEST_OPED,
        verbose_name='Program Tier',
        help_text='Which Byline program are you applying for?',
    )

    # ── Content proposal ──────────────────────
    topic_idea = models.TextField(
        verbose_name='Article / Content Idea',
        help_text=(
            'What do you want to write about? Give us a topic, an angle, and why our readers need to read it. '
            'Even a few sentences is enough to start.'
        ),
    )
    # Replace the old writing_sample URLField with this FileField:
    writing_sample = models.FileField(
        upload_to='writing_samples/%Y/%m/', # Organizes files by year and month in your media folder
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_file_size
        ],
        verbose_name='Writing Sample (PDF)',
        help_text='Upload a PDF sample (Max 5MB).',
    )

    # ── Online presence ───────────────────────
    linkedin_url = models.URLField(
        blank=True,
        verbose_name='LinkedIn Profile URL',
    )
    website_url = models.URLField(
        blank=True,
        verbose_name='Website / Portfolio URL',
    )

    # ── For Brand Collab tier only ────────────
    brand_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Brand / Client Name',
        help_text='Only required for Brand Collab applicants.',
    )
    monthly_volume = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Expected Monthly Article Volume',
        help_text='Approximate number of articles per month — Brand Collab only.',
    )

    # ── Consent ───────────────────────────────
    consent_publish = models.BooleanField(
        default=False,
        verbose_name='Consent to Publish',
        help_text=(
            'I understand that published articles will carry my byline and may be '
            'shared across Corporate Impact\'s print, digital, and social channels.'
        ),
    )

    # ── Admin / workflow ──────────────────────
    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        verbose_name='Lead Status',
    )
    internal_notes = models.TextField(
        blank=True,
        verbose_name='Internal Notes',
        help_text='Editorial team use only — not visible to the applicant.',
    )
    assigned_to = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Assigned Editor',
        help_text='Name of the editor handling this lead.',
    )

    # ── Timestamps ────────────────────────────
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Submitted At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    class Meta:
        verbose_name        = 'Byline Lead'
        verbose_name_plural = 'Byline Leads'
        ordering            = ['-created_at']
        indexes             = [
            models.Index(fields=['status']),
            models.Index(fields=['tier']),
            models.Index(fields=['created_at']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f'{self.name} — {self.get_tier_display()} ({self.get_status_display()})'

    @property
    def is_brand_collab(self):
        return self.tier == self.Tier.BRAND_COLLAB

    @property
    def is_new(self):
        return self.status == LeadStatus.NEW

    @property
    def is_approved(self):
        return self.status == LeadStatus.APPROVED