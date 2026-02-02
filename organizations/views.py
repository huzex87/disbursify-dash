"""
Organization Views
"""
import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Organization, TeamMember
from .serializers import (
    OrganizationSerializer, OrganizationCreateSerializer,
    TeamMemberSerializer, TeamMemberInviteSerializer
)

User = get_user_model()


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Organization CRUD operations.
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrganizationCreateSerializer
        return OrganizationSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Get organizations where user is owner or team member
        owned = Organization.objects.filter(owner=user, deleted_at__isnull=True)
        member_of = Organization.objects.filter(
            team_members__user=user,
            team_members__status='active',
            deleted_at__isnull=True
        )
        
        return (owned | member_of).distinct()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        
        return Response({
            'success': True,
            'data': OrganizationSerializer(org).data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Only owner can update
        if instance.owner != request.user:
            return Response({
                'success': False,
                'error': {'code': 'FORBIDDEN', 'message': 'Only the owner can update this organization'}
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['get', 'post'])
    def team(self, request, pk=None):
        """Get team members or invite new member."""
        org = self.get_object()
        
        if request.method == 'GET':
            members = TeamMember.objects.filter(
                organization=org
            ).exclude(status='removed')
            
            serializer = TeamMemberSerializer(members, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        
        elif request.method == 'POST':
            # Check permission
            membership = TeamMember.objects.filter(
                organization=org,
                user=request.user,
                status='active'
            ).first()
            
            if not membership or not membership.has_permission('manage_team'):
                return Response({
                    'success': False,
                    'error': {'code': 'FORBIDDEN', 'message': 'No permission to manage team'}
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Check team member limit
            current_count = TeamMember.objects.filter(
                organization=org, 
                status='active'
            ).count()
            
            limits = org.get_tier_limits()
            if limits['team_members'] != -1 and current_count >= limits['team_members']:
                return Response({
                    'success': False,
                    'error': {'code': 'LIMIT_REACHED', 'message': 'Team member limit reached for your plan'}
                }, status=status.HTTP_403_FORBIDDEN)
            
            serializer = TeamMemberInviteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            
            # Check if already member
            email = data['email']
            existing = TeamMember.objects.filter(
                organization=org,
                invited_email=email,
                status__in=['pending', 'active']
            ).first()
            
            if existing:
                return Response({
                    'success': False,
                    'error': {'code': 'ALREADY_MEMBER', 'message': 'This user is already a team member or has a pending invite'}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create invitation
            token = secrets.token_urlsafe(32)
            member = TeamMember.objects.create(
                organization=org,
                invited_email=email,
                invited_by=request.user,
                invited_at=timezone.now(),
                invitation_token=token,
                invitation_expires_at=timezone.now() + timedelta(days=7),
                role=data['role'],
                business_access=data.get('business_access', []),
                status='pending'
            )
            
            # TODO: Send invitation email
            
            return Response({
                'success': True,
                'data': TeamMemberSerializer(member).data,
                'message': f'Invitation sent to {email}'
            }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'], url_path='team/(?P<member_id>[^/.]+)')
    def remove_member(self, request, pk=None, member_id=None):
        """Remove a team member."""
        org = self.get_object()
        
        # Check permission
        membership = TeamMember.objects.filter(
            organization=org,
            user=request.user,
            status='active'
        ).first()
        
        if not membership or not membership.has_permission('manage_team'):
            return Response({
                'success': False,
                'error': {'code': 'FORBIDDEN', 'message': 'No permission to manage team'}
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            member = TeamMember.objects.get(id=member_id, organization=org)
            
            # Can't remove owner
            if member.role == 'owner':
                return Response({
                    'success': False,
                    'error': {'code': 'FORBIDDEN', 'message': 'Cannot remove organization owner'}
                }, status=status.HTTP_403_FORBIDDEN)
            
            member.status = 'removed'
            member.save()
            
            return Response({'success': True, 'data': None})
            
        except TeamMember.DoesNotExist:
            return Response({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Team member not found'}
            }, status=status.HTTP_404_NOT_FOUND)
