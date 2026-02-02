"""
Custom User Model for Disbursify Dash
"""
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone as dj_timezone


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email_verified', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for Disbursify Dash.
    Uses email as the primary identifier instead of username.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Authentication
    email = models.EmailField(unique=True, max_length=255)
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    
    # Profile
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    
    # Preferences
    user_timezone = models.CharField(max_length=50, default='Africa/Lagos')
    locale = models.CharField(max_length=10, default='en-NG')
    preferences = models.JSONField(default=dict, blank=True)
    
    # Security
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=255, blank=True, null=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    # Django required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=dj_timezone.now)
    
    # Soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def is_locked(self):
        """Check if user account is locked."""
        if self.locked_until and self.locked_until > dj_timezone.now():
            return True
        return False
    
    def record_login(self, ip_address=None):
        """Record successful login."""
        self.last_login_at = dj_timezone.now()
        self.last_login_ip = ip_address
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=['last_login_at', 'last_login_ip', 'failed_login_attempts', 'locked_until'])
    
    def record_failed_login(self):
        """Record failed login attempt."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = dj_timezone.now() + dj_timezone.timedelta(minutes=30)
        self.save(update_fields=['failed_login_attempts', 'locked_until'])


class OTPCode(models.Model):
    """Store OTP codes for phone/email verification."""
    
    OTP_TYPES = [
        ('phone_verification', 'Phone Verification'),
        ('email_verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
        ('login_2fa', 'Two-Factor Login'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # For unregistered users verifying phone
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    code = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPES)
    
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'otp_codes'
        indexes = [
            models.Index(fields=['phone', 'otp_type', 'is_used']),
            models.Index(fields=['email', 'otp_type', 'is_used']),
        ]
    
    def is_expired(self):
        return dj_timezone.now() > self.expires_at
    
    def is_valid(self):
        return not self.is_used and not self.is_expired() and self.attempts < 3
