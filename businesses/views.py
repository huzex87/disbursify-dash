"""
Business Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from organizations.models import Organization, TeamMember
from .models import Business, BankAccount
from .serializers import (
    BusinessSerializer, BusinessSummarySerializer,
    BankAccountSerializer, BankAccountCreateSerializer
)


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business CRUD operations.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessSerializer
    
    def get_queryset(self):
        user = self.request.user
        org_id = self.request.query_params.get('organization_id')
        
        if not org_id:
            # Return businesses from all accessible orgs
            orgs = Organization.objects.filter(
                team_members__user=user,
                team_members__status='active'
            ).values_list('id', flat=True)
            
            return Business.objects.filter(
                organization_id__in=orgs,
                archived_at__isnull=True
            )
        
        # Check org access
        membership = TeamMember.objects.filter(
            organization_id=org_id,
            user=user,
            status='active'
        ).first()
        
        if not membership:
            return Business.objects.none()
        
        # Filter by business access if not admin/owner
        qs = Business.objects.filter(
            organization_id=org_id,
            archived_at__isnull=True
        )
        
        if membership.role not in ['owner', 'admin'] and membership.business_access:
            qs = qs.filter(id__in=membership.business_access)
        
        return qs
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('name')
        serializer = BusinessSummarySerializer(queryset, many=True)
        
        # Calculate totals
        total_balance = sum(float(b.current_balance or 0) for b in queryset)
        
        return Response({
            'success': True,
            'data': {
                'businesses': serializer.data,
                'summary': {
                    'count': len(serializer.data),
                    'total_balance': total_balance,
                    'currency': 'NGN'
                }
            }
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        org_id = request.data.get('organization_id')
        
        if not org_id:
            return Response({
                'success': False,
                'error': {'code': 'MISSING_ORG', 'message': 'organization_id is required'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check permission
        membership = TeamMember.objects.filter(
            organization_id=org_id,
            user=request.user,
            status='active'
        ).first()
        
        if not membership or not membership.has_permission('manage_businesses'):
            return Response({
                'success': False,
                'error': {'code': 'FORBIDDEN', 'message': 'No permission to create businesses'}
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check business limit
        org = Organization.objects.get(id=org_id)
        current_count = Business.objects.filter(
            organization=org,
            archived_at__isnull=True
        ).count()
        
        limits = org.get_tier_limits()
        if limits['businesses'] != -1 and current_count >= limits['businesses']:
            return Response({
                'success': False,
                'error': {'code': 'LIMIT_REACHED', 'message': f'Business limit ({limits["businesses"]}) reached for your plan'}
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'organization': org}
        )
        serializer.is_valid(raise_exception=True)
        business = serializer.save()
        
        return Response({
            'success': True,
            'data': self.get_serializer(business).data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive a business."""
        business = self.get_object()
        from django.utils import timezone
        business.archived_at = timezone.now()
        business.archived_by = request.user
        business.is_active = False
        business.save()
        
        return Response({
            'success': True,
            'data': {'message': f'{business.name} has been archived'}
        })
    
    @action(detail=True, methods=['get', 'post'])
    def bank_accounts(self, request, pk=None):
        """Get or connect bank accounts."""
        business = self.get_object()
        
        if request.method == 'GET':
            accounts = BankAccount.objects.filter(business=business)
            serializer = BankAccountSerializer(accounts, many=True)
            return Response({
                'success': True,
                'data': serializer.data
            })
        
        elif request.method == 'POST':
            serializer = BankAccountCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            
            if data['provider'] == 'manual':
                # Create manual bank account
                account = BankAccount.objects.create(
                    business=business,
                    organization=business.organization,
                    bank_name=data.get('bank_name', ''),
                    account_number=data.get('account_number', ''),
                    account_name=data.get('account_name', ''),
                    provider='manual',
                    sync_status='disconnected',
                    connected_by=request.user
                )
            else:
                # TODO: Exchange access_code with Mono/Okra for account details
                return Response({
                    'success': False,
                    'error': {'code': 'NOT_IMPLEMENTED', 'message': 'Bank integration coming soon'}
                }, status=status.HTTP_501_NOT_IMPLEMENTED)
            
            return Response({
                'success': True,
                'data': BankAccountSerializer(account).data
            }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def recalculate_balance(self, request, pk=None):
        """Force recalculate business balance."""
        business = self.get_object()
        new_balance = business.recalculate_balance()
        
        return Response({
            'success': True,
            'data': {
                'current_balance': float(new_balance),
                'balance_updated_at': business.balance_updated_at.isoformat()
            }
        })
