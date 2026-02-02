"""
Alert Models
"""
import uuid
from django.db import models
from django.conf import settings
from organizations.models import Organization
from businesses.models import Business


class AlertRule(models.Model):
    """
    Rules for triggering alerts.
    """
    
    ALERT_TYPES = [
        ('low_cash', 'Low Cash Warning'),
        ('unusual_expense', 'Unusual Expense'),
        ('large_transaction', 'Large Transaction'),
        ('sync_failed', 'Sync Failed'),
        ('daily_summary', 'Daily Summary'),
        ('goal_achieved', 'Goal Achieved'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='alert_rules'
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alert_rules'
    )  # NULL = applies to all
    
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    conditions = models.JSONField(default=dict)
    
    # Notification channels
    notify_email = models.BooleanField(default=True)
    notify_sms = models.BooleanField(default=False)
    notify_push = models.BooleanField(default=True)
    notify_whatsapp = models.BooleanField(default=False)
    
    recipients = models.JSONField(default=list, blank=True)  # User UUIDs
    schedule = models.JSONField(default=dict, blank=True)
    
    is_active = models.BooleanField(default=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    trigger_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'alert_rules'
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['alert_type', 'is_active']),
        ]


class Alert(models.Model):
    """
    Generated alerts from rules.
    """
    
    SEVERITY = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS = [
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('actioned', 'Actioned'),
        ('dismissed', 'Dismissed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    alert_rule = models.ForeignKey(
        AlertRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alerts'
    )
    
    alert_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20, choices=SEVERITY, default='medium')
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    context_data = models.JSONField(default=dict, blank=True)
    action_url = models.URLField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS, default='unread')
    read_at = models.DateTimeField(null=True, blank=True)
    read_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='read_alerts'
    )
    actioned_at = models.DateTimeField(null=True, blank=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    dismissed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dismissed_alerts'
    )
    
    # Notifications sent
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    sms_sent = models.BooleanField(default=False)
    sms_sent_at = models.DateTimeField(null=True, blank=True)
    push_sent = models.BooleanField(default=False)
    push_sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'status', '-created_at']),
            models.Index(fields=['business']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"[{self.severity}] {self.title}"
