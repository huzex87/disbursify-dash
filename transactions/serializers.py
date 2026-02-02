"""
Transaction Serializers
"""
from rest_framework import serializers
from .models import Transaction, Category, Receipt


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories."""
    
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'category_type',
            'icon', 'color', 'sort_order', 'is_system', 'is_active',
            'subcategories'
        ]
    
    def get_subcategories(self, obj):
        if hasattr(obj, 'subcategories'):
            return CategorySerializer(obj.subcategories.filter(is_active=True), many=True).data
        return []


class ReceiptSerializer(serializers.ModelSerializer):
    """Serializer for receipts."""
    
    class Meta:
        model = Receipt
        fields = ['id', 'file_name', 'file_url', 'file_size', 'mime_type', 'thumbnail_url', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction details."""
    
    business_name = serializers.CharField(source='business.name', read_only=True)
    receipts = ReceiptSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'business', 'business_name',
            'transaction_date', 'transaction_type',
            'amount', 'currency', 'exchange_rate', 'amount_ngn',
            'category', 'subcategory', 'description', 'notes',
            'reference_number', 'payment_method', 'payment_reference',
            'status', 'is_reconciled', 'tags',
            'has_receipt', 'receipts',
            'ai_categorized', 'ai_confidence', 'ai_suggested_category',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'amount_ngn', 'status', 'is_reconciled', 
            'ai_categorized', 'ai_confidence', 'ai_suggested_category',
            'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        organization = validated_data['business'].organization
        
        return Transaction.objects.create(
            organization=organization,
            created_by=user,
            **validated_data
        )


class TransactionListSerializer(serializers.ModelSerializer):
    """Light serializer for list views."""
    
    business_name = serializers.CharField(source='business.name', read_only=True)
    business_color = serializers.CharField(source='business.color', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'business', 'business_name', 'business_color',
            'transaction_date', 'transaction_type',
            'amount', 'currency', 'amount_ngn',
            'category', 'description', 'status', 'has_receipt'
        ]


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating transactions."""
    
    class Meta:
        model = Transaction
        fields = [
            'business', 'transaction_date', 'transaction_type',
            'amount', 'currency', 'exchange_rate',
            'category', 'subcategory', 'description', 'notes',
            'reference_number', 'payment_method', 'payment_reference', 'tags'
        ]
    
    def validate_business(self, value):
        # Will be validated in view
        return value
