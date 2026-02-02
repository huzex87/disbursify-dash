"""
Admin configuration for Disbursify Dash.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User, OTPCode
from organizations.models import Organization, TeamMember
from businesses.models import Business, BankAccount
from transactions.models import Transaction, Category, Receipt
from alerts.models import AlertRule, Alert


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'email_verified', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'email_verified', 'two_factor_enabled']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'phone', 'avatar_url')}),
        ('Verification', {'fields': ('email_verified', 'phone_verified', 'two_factor_enabled')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Security', {'fields': ('failed_login_attempts', 'locked_until', 'last_login_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'subscription_tier', 'subscription_status', 'created_at']
    list_filter = ['subscription_tier', 'subscription_status']
    search_fields = ['name', 'owner__email']
    raw_id_fields = ['owner']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['organization', 'user', 'invited_email', 'role', 'status']
    list_filter = ['role', 'status']
    search_fields = ['organization__name', 'user__email', 'invited_email']
    raw_id_fields = ['organization', 'user', 'invited_by']


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'industry', 'current_balance', 'is_active', 'created_at']
    list_filter = ['industry', 'is_active']
    search_fields = ['name', 'organization__name']
    raw_id_fields = ['organization', 'created_by']


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_number', 'business', 'provider', 'sync_status']
    list_filter = ['provider', 'sync_status']
    search_fields = ['bank_name', 'account_number', 'business__name']
    raw_id_fields = ['business', 'organization']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_date', 'business', 'transaction_type', 'amount', 'category', 'status']
    list_filter = ['transaction_type', 'status', 'payment_method']
    search_fields = ['description', 'reference_number', 'business__name']
    date_hierarchy = 'transaction_date'
    raw_id_fields = ['organization', 'business', 'created_by']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'is_system', 'is_active', 'sort_order']
    list_filter = ['category_type', 'is_system', 'is_active']
    search_fields = ['name', 'slug']


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'transaction', 'created_at']
    search_fields = ['file_name']
    raw_id_fields = ['transaction', 'organization']


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'alert_type', 'is_active']
    list_filter = ['alert_type', 'is_active']
    raw_id_fields = ['organization', 'business']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'alert_type', 'severity', 'status', 'created_at']
    list_filter = ['alert_type', 'severity', 'status']
    search_fields = ['title', 'message']
    raw_id_fields = ['organization', 'business', 'alert_rule']


# Register remaining models
admin.site.register(OTPCode)

# Admin site customization
admin.site.site_header = 'Disbursify Dash Admin'
admin.site.site_title = 'Disbursify Dash'
admin.site.index_title = 'Dashboard'
