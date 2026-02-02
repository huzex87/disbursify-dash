"""
Transaction and Category Models
"""
import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from organizations.models import Organization
from businesses.models import Business, BankAccount


class Category(models.Model):
    """
    Transaction categories. System defaults + custom per organization.
    """
    
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='categories'
    )  # NULL = system default
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    is_system = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']
        unique_together = [['organization', 'slug']]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['category_type']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class Transaction(models.Model):
    """
    Financial transaction record.
    """
    
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('pos', 'POS'),
        ('cheque', 'Cheque'),
        ('mobile_money', 'Mobile Money'),
        ('online', 'Online Payment'),
    ]
    
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('reconciled', 'Reconciled'),
        ('voided', 'Voided'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    
    # Core
    transaction_date = models.DateField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # Amount
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, default=1.0)
    amount_ngn = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Classification
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    
    # Details
    description = models.TextField()
    notes = models.TextField(blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Payment
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, blank=True, null=True)
    payment_reference = models.CharField(max_length=255, blank=True, null=True)
    
    # Transfer fields
    transfer_to_business = models.ForeignKey(
        Business,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incoming_transfers'
    )
    transfer_pair = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paired_transfer'
    )
    
    # Bank Sync
    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    bank_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    bank_narration = models.TextField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=50, choices=STATUS, default='confirmed')
    is_reconciled = models.BooleanField(default=False)
    reconciled_at = models.DateTimeField(null=True, blank=True)
    reconciled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reconciled_transactions'
    )
    
    # AI Categorization
    ai_categorized = models.BooleanField(default=False)
    ai_confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ai_suggested_category = models.CharField(max_length=100, blank=True, null=True)
    user_corrected = models.BooleanField(default=False)
    
    # Receipt
    has_receipt = models.BooleanField(default=False)
    
    # Tags
    tags = models.JSONField(default=list, blank=True)
    
    # Audit
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_transactions'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_transactions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Void
    voided_at = models.DateTimeField(null=True, blank=True)
    voided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voided_transactions'
    )
    void_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['organization', '-transaction_date']),
            models.Index(fields=['business', '-transaction_date']),
            models.Index(fields=['organization', 'category']),
            models.Index(fields=['organization', 'transaction_type', 'transaction_date']),
            models.Index(fields=['status']),
            models.Index(fields=['bank_transaction_id']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type}: {self.currency} {self.amount} - {self.description[:50]}"
    
    def save(self, *args, **kwargs):
        # Calculate NGN amount
        if self.currency == 'NGN':
            self.amount_ngn = self.amount
        else:
            self.amount_ngn = self.amount * Decimal(str(self.exchange_rate))
        
        super().save(*args, **kwargs)
        
        # Update business balance
        self.business.recalculate_balance()


class Receipt(models.Model):
    """
    Receipt attachments for transactions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='receipts'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='receipts'
    )
    
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()
    file_size = models.PositiveIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    
    thumbnail_url = models.URLField(blank=True, null=True)
    ocr_text = models.TextField(blank=True, null=True)
    ocr_processed_at = models.DateTimeField(null=True, blank=True)
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'receipts'
        indexes = [
            models.Index(fields=['transaction']),
            models.Index(fields=['organization']),
        ]
    
    def __str__(self):
        return self.file_name
