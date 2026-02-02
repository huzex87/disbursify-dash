"""
Organization Serializers
"""
from rest_framework import serializers
from .models import Organization, TeamMember
from accounts.serializers import UserSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for organization details."""
    
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    business_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    tier_limits = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'slug', 'logo_url',
            'subscription_tier', 'subscription_status',
            'trial_ends_at', 'subscription_ends_at',
            'max_businesses', 'max_team_members', 'features_enabled',
            'owner_email', 'business_count', 'member_count', 'tier_limits',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'subscription_tier', 'subscription_status', 'created_at', 'updated_at']
    
    def get_business_count(self, obj):
        return obj.businesses.filter(is_active=True).count()
    
    def get_member_count(self, obj):
        return obj.team_members.filter(status='active').count()
    
    def get_tier_limits(self, obj):
        return obj.get_tier_limits()


class OrganizationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating an organization."""
    
    class Meta:
        model = Organization
        fields = ['name', 'logo_url']
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        # Create organization with 14-day trial
        from django.utils import timezone
        org = Organization.objects.create(
            owner=user,
            trial_ends_at=timezone.now() + timezone.timedelta(days=14),
            **validated_data
        )
        
        # Create owner as team member
        TeamMember.objects.create(
            organization=org,
            user=user,
            role='owner',
            status='active',
            accepted_at=timezone.now()
        )
        
        return org


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for team member details."""
    
    user = UserSerializer(read_only=True)
    inviter = UserSerializer(source='invited_by', read_only=True)
    
    class Meta:
        model = TeamMember
        fields = [
            'id', 'user', 'invited_email', 'role', 'status',
            'business_access', 'inviter', 'invited_at', 'accepted_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'invited_at', 'accepted_at', 'created_at', 'updated_at']


class TeamMemberInviteSerializer(serializers.Serializer):
    """Serializer for inviting team members."""
    
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=['admin', 'accountant', 'manager', 'viewer'])
    business_access = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        default=list
    )
