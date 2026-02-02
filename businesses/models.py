"""
Business Model
"""
import uuid
from django.db import models
from django.conf import settings
from organizations.models import Organization


class Business(models.Model):
    """
    Business entity belonging to an organization.
    Each business tracks its own transactions, accounts, and financials.
    """
    
    INDUSTRIES = [
        ('restaurant', 'Restaurant/Food'),
        ('retail', 'Retail/Shop'),
        ('transport', 'Transport/Logistics'),
        ('real_estate', 'Real Estate'),
        ('consulting', 'Consulting/Services'),
        ('agriculture', 'Agriculture'),
        ('manufacturing', 'Manufacturing'),
        ('technology', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('hospitality', 'Hospitality'),
        ('fashion', 'Fashion/Beauty'),
        ('construction', 'Construction'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]
    
    BUSINESS_TYPES = [
        ('sole_proprietorship', 'Sole Proprietorship'),
        ('partnership', 'Partnership'),
        ('limited_liability', 'Limited Liability Company'),
        ('plc', 'Public Limited Company'),
        ('cooperative', 'Cooperative'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='businesses'
    )
    
    # Basic Info
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    # Classification
    industry = models.CharField(max_length=50, choices=INDUSTRIES, default='other')
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES, blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Branding
    logo_url = models.URLField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#6B21A8')  # Hex color
    icon = models.CharField(max_length=50, blank=True, null=True)
    
    # Financial Settings
    primary_currency = models.CharField(max_length=3, default='NGN')
    fiscal_year_start = models.DateField(null=True, blank=True)
    
    # Opening Balances
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    opening_balance_date = models.DateField(null=True, blank=True)
    
    # Cached Calculations (updated by triggers/tasks)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance_updated_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='archived_businesses'
    )
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_businesses'
    )
    
    class Meta:
        db_table = 'businesses'
        verbose_name_plural = 'Businesses'
        ordering = ['name']
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['organization', 'is_active']),
            models.Index(fields=['industry']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.organization.name})"
    
    def recalculate_balance(self):
        """Recalculate current balance from all transactions."""
        from transactions.models import Transaction
        from django.db.models import Sum, Case, When, F, DecimalField
        
        result = Transaction.objects.filter(
            business=self,
            status='confirmed'
        ).aggregate(
            total=Sum(
                Case(
                    When(transaction_type='income', then=F('amount_ngn')),
                    When(transaction_type='expense', then=-F('amount_ngn')),
                    default=0,
                    output_field=DecimalField()
                )
            )
        )
        
        from django.utils import timezone
        self.current_balance = (result['total'] or 0) + self.opening_balance
        self.balance_updated_at = timezone.now()
        self.save(update_fields=['current_balance', 'balance_updated_at'])
        
        return self.current_balance


class BankAccount(models.Model):
    """
    Bank account linked to a business for automatic transaction sync.
    """
    
    PROVIDERS = [
        ('mono', 'Mono'),
        ('okra', 'Okra'),
        ('manual', 'Manual'),
    ]
    
    SYNC_STATUS = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('failed', 'Failed'),
        ('disconnected', 'Disconnected'),
    ]
    
    ACCOUNT_TYPES = [
        ('current', 'Current Account'),
        ('savings', 'Savings Account'),
        ('domiciliary', 'Domiciliary Account'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )
    
    # Bank Info
    bank_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=20, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=20)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, blank=True, null=True)
    currency = models.CharField(max_length=3, default='NGN')
    
    # Provider Integration
    provider = models.CharField(max_length=50, choices=PROVIDERS, default='manual')
    provider_account_id = models.CharField(max_length=255, blank=True, null=True)
    provider_institution_id = models.CharField(max_length=255, blank=True, null=True)
    provider_access_token = models.TextField(blank=True, null=True)  # Encrypted
    provider_refresh_token = models.TextField(blank=True, null=True)  # Encrypted
    
    # Sync Status
    sync_status = models.CharField(max_length=50, choices=SYNC_STATUS, default='active')
    last_synced_at = models.DateTimeField(null=True, blank=True)
    last_sync_error = models.TextField(blank=True, null=True)
    next_sync_at = models.DateTimeField(null=True, blank=True)
    
    # Balance
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    available_balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    balance_updated_at = models.DateTimeField(null=True, blank=True)
    
    # Settings
    is_primary = models.BooleanField(default=False)
    auto_sync_enabled = models.BooleanField(default=True)
    sync_frequency_minutes = models.PositiveIntegerField(default=60)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    connected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='connected_bank_accounts'
    )
    disconnected_at = models.DateTimeField(null=True, blank=True)
    disconnected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='disconnected_bank_accounts'
    )
    
    class Meta:
        db_table = 'bank_accounts'
        indexes = [
            models.Index(fields=['business']),
            models.Index(fields=['organization']),
            models.Index(fields=['sync_status', 'next_sync_at']),
        ]
        unique_together = [['provider', 'provider_account_id']]
    
    def __str__(self):
        masked = f"****{self.account_number[-4:]}" if len(self.account_number) >= 4 else self.account_number
        return f"{self.bank_name} - {masked}"
