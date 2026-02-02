"""
Organization and Team Member Models
"""
import uuid
from django.db import models
from django.conf import settings


class Organization(models.Model):
    """
    Organization represents a customer account.
    One user can own one organization, which contains multiple businesses.
    """
    
    SUBSCRIPTION_TIERS = [
        ('starter', 'Starter'),
        ('growth', 'Growth'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
    ]
    
    SUBSCRIPTION_STATUS = [
        ('trialing', 'Trialing'),
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('unpaid', 'Unpaid'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_organizations'
    )
    
    # Details
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    
    # Subscription
    subscription_tier = models.CharField(max_length=50, choices=SUBSCRIPTION_TIERS, default='starter')
    subscription_status = models.CharField(max_length=50, choices=SUBSCRIPTION_STATUS, default='trialing')
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    subscription_ends_at = models.DateTimeField(null=True, blank=True)
    
    # Limits
    max_businesses = models.PositiveIntegerField(default=3)
    max_team_members = models.PositiveIntegerField(default=1)
    features_enabled = models.JSONField(default=dict, blank=True)
    
    # Billing
    billing_email = models.EmailField(blank=True, null=True)
    billing_address = models.JSONField(default=dict, blank=True)
    paystack_customer_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Settings
    settings = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'organizations'
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['slug']),
            models.Index(fields=['subscription_status']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        return self.subscription_status in ['trialing', 'active']
    
    def get_tier_limits(self):
        """Return limits based on subscription tier."""
        limits = {
            'starter': {'businesses': 3, 'team_members': 1, 'bank_sync': False},
            'growth': {'businesses': 10, 'team_members': 5, 'bank_sync': True},
            'business': {'businesses': -1, 'team_members': 20, 'bank_sync': True},  # -1 = unlimited
            'enterprise': {'businesses': -1, 'team_members': -1, 'bank_sync': True},
        }
        return limits.get(self.subscription_tier, limits['starter'])


class TeamMember(models.Model):
    """
    Team members with role-based access to an organization.
    """
    
    ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('accountant', 'Accountant'),
        ('manager', 'Manager'),
        ('viewer', 'Viewer'),
    ]
    
    STATUS = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('removed', 'Removed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='team_members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='team_memberships'
    )
    
    # Invitation
    invited_email = models.EmailField(blank=True, null=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invitations_sent'
    )
    invited_at = models.DateTimeField(null=True, blank=True)
    invitation_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    invitation_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Role & Permissions
    role = models.CharField(max_length=50, choices=ROLES, default='viewer')
    business_access = models.JSONField(default=list, blank=True)  # List of business UUIDs
    permissions_override = models.JSONField(default=dict, blank=True)
    
    # Status
    status = models.CharField(max_length=50, choices=STATUS, default='pending')
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'team_members'
        unique_together = [['organization', 'user']]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        if self.user:
            return f"{self.user.email} - {self.organization.name} ({self.role})"
        return f"{self.invited_email} - {self.organization.name} (pending)"
    
    def has_permission(self, permission):
        """Check if team member has a specific permission."""
        role_permissions = {
            'owner': ['*'],  # All permissions
            'admin': ['manage_team', 'manage_businesses', 'add_transactions', 
                     'edit_transactions', 'delete_transactions', 'view_reports', 'export'],
            'accountant': ['add_transactions', 'edit_transactions', 'view_reports', 'export'],
            'manager': ['view_reports', 'add_transactions'],
            'viewer': ['view_reports'],
        }
        
        # Check override first
        if permission in self.permissions_override:
            return self.permissions_override[permission]
        
        # Check role permissions
        perms = role_permissions.get(self.role, [])
        return '*' in perms or permission in perms
