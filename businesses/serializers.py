"""
Business Serializers
"""
from rest_framework import serializers
from .models import Business, BankAccount


class BusinessSerializer(serializers.ModelSerializer):
    """Serializer for business details."""
    
    transaction_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'short_name', 'description',
            'industry', 'business_type', 'registration_number',
            'logo_url', 'color', 'icon',
            'primary_currency', 'fiscal_year_start',
            'opening_balance', 'opening_balance_date',
            'current_balance', 'balance_updated_at',
            'is_active', 'transaction_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'current_balance', 'balance_updated_at', 'created_at', 'updated_at']
    
    def get_transaction_count(self, obj):
        return obj.transactions.filter(status='confirmed').count()
    
    def create(self, validated_data):
        organization = self.context.get('organization')
        user = self.context['request'].user
        
        return Business.objects.create(
            organization=organization,
            created_by=user,
            **validated_data
        )


class BusinessSummarySerializer(serializers.ModelSerializer):
    """Light serializer for list views."""
    
    class Meta:
        model = Business
        fields = ['id', 'name', 'short_name', 'industry', 'color', 'icon', 'current_balance', 'is_active']


class BankAccountSerializer(serializers.ModelSerializer):
    """Serializer for bank account details."""
    
    masked_account_number = serializers.SerializerMethodField()
    
    class Meta:
        model = BankAccount
        fields = [
            'id', 'bank_name', 'bank_code', 'account_name',
            'masked_account_number', 'account_type', 'currency',
            'provider', 'sync_status', 'last_synced_at',
            'current_balance', 'available_balance', 'balance_updated_at',
            'is_primary', 'auto_sync_enabled',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'provider', 'sync_status', 'last_synced_at', 
                          'current_balance', 'available_balance', 'balance_updated_at',
                          'created_at', 'updated_at']
    
    def get_masked_account_number(self, obj):
        if len(obj.account_number) >= 4:
            return f"****{obj.account_number[-4:]}"
        return obj.account_number


class BankAccountCreateSerializer(serializers.Serializer):
    """Serializer for connecting bank via Mono/Okra."""
    
    provider = serializers.ChoiceField(choices=['mono', 'okra', 'manual'])
    access_code = serializers.CharField(required=False)  # From Mono/Okra widget
    
    # For manual accounts
    bank_name = serializers.CharField(required=False)
    account_number = serializers.CharField(required=False)
    account_name = serializers.CharField(required=False)
