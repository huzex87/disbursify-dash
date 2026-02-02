"""
Transaction Views
"""
from django.db.models import Sum, Case, When, F, DecimalField
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from organizations.models import TeamMember
from businesses.models import Business
from .models import Transaction, Category, Receipt
from .serializers import (
    TransactionSerializer, TransactionListSerializer, TransactionCreateSerializer,
    CategorySerializer, ReceiptSerializer
)


class TransactionFilter(filters.FilterSet):
    """Filters for transaction list."""
    
    business = filters.UUIDFilter(field_name='business_id')
    transaction_type = filters.ChoiceFilter(choices=Transaction.TRANSACTION_TYPES)
    category = filters.CharFilter(field_name='category')
    status = filters.ChoiceFilter(choices=Transaction.STATUS)
    date_from = filters.DateFilter(field_name='transaction_date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='transaction_date', lookup_expr='lte')
    min_amount = filters.NumberFilter(field_name='amount_ngn', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount_ngn', lookup_expr='lte')
    
    class Meta:
        model = Transaction
        fields = ['business', 'transaction_type', 'category', 'status']


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Transaction CRUD operations.
    """
    permission_classes = [IsAuthenticated]
    filterset_class = TransactionFilter
    search_fields = ['description', 'notes', 'category', 'reference_number']
    ordering_fields = ['transaction_date', 'amount_ngn', 'created_at']
    ordering = ['-transaction_date', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TransactionListSerializer
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    def get_queryset(self):
        user = self.request.user
        org_id = self.request.query_params.get('organization_id')
        
        # Get accessible business IDs
        memberships = TeamMember.objects.filter(
            user=user,
            status='active'
        )
        
        if org_id:
            memberships = memberships.filter(organization_id=org_id)
        
        accessible_businesses = []
        for m in memberships:
            if m.role in ['owner', 'admin']:
                # Can access all businesses in org
                business_ids = Business.objects.filter(
                    organization=m.organization,
                    archived_at__isnull=True
                ).values_list('id', flat=True)
                accessible_businesses.extend(business_ids)
            elif m.business_access:
                accessible_businesses.extend(m.business_access)
        
        return Transaction.objects.filter(
            business_id__in=accessible_businesses,
            status__in=['pending', 'confirmed', 'reconciled']
        ).select_related('business')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Calculate summary
        summary = queryset.aggregate(
            total_income=Sum(
                Case(
                    When(transaction_type='income', then=F('amount_ngn')),
                    default=0,
                    output_field=DecimalField()
                )
            ),
            total_expense=Sum(
                Case(
                    When(transaction_type='expense', then=F('amount_ngn')),
                    default=0,
                    output_field=DecimalField()
                )
            )
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data = {
                'success': True,
                'data': {
                    'transactions': response.data['results'],
                    'summary': {
                        'total_income': float(summary['total_income'] or 0),
                        'total_expense': float(summary['total_expense'] or 0),
                        'net': float((summary['total_income'] or 0) - (summary['total_expense'] or 0)),
                        'count': queryset.count()
                    },
                    'pagination': {
                        'count': response.data['count'],
                        'next': response.data['next'],
                        'previous': response.data['previous']
                    }
                }
            }
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': {
                'transactions': serializer.data,
                'summary': {
                    'total_income': float(summary['total_income'] or 0),
                    'total_expense': float(summary['total_expense'] or 0),
                    'net': float((summary['total_income'] or 0) - (summary['total_expense'] or 0)),
                    'count': queryset.count()
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verify business access
        business = serializer.validated_data['business']
        membership = TeamMember.objects.filter(
            organization=business.organization,
            user=request.user,
            status='active'
        ).first()
        
        if not membership or not membership.has_permission('add_transactions'):
            return Response({
                'success': False,
                'error': {'code': 'FORBIDDEN', 'message': 'No permission to add transactions'}
            }, status=status.HTTP_403_FORBIDDEN)
        
        transaction = Transaction.objects.create(
            organization=business.organization,
            created_by=request.user,
            **serializer.validated_data
        )
        
        return Response({
            'success': True,
            'data': TransactionSerializer(transaction).data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        
        serializer = TransactionCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Can't edit voided transactions
        if instance.status == 'voided':
            return Response({
                'success': False,
                'error': {'code': 'VOIDED', 'message': 'Cannot edit voided transactions'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(updated_by=request.user)
        
        return Response({
            'success': True,
            'data': TransactionSerializer(instance).data
        })
    
    @action(detail=True, methods=['post'])
    def void(self, request, pk=None):
        """Void a transaction."""
        transaction = self.get_object()
        
        if transaction.status == 'voided':
            return Response({
                'success': False,
                'error': {'code': 'ALREADY_VOIDED', 'message': 'Transaction already voided'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        from django.utils import timezone
        transaction.status = 'voided'
        transaction.voided_at = timezone.now()
        transaction.voided_by = request.user
        transaction.void_reason = request.data.get('reason', '')
        transaction.save()
        
        # Recalculate business balance
        transaction.business.recalculate_balance()
        
        return Response({
            'success': True,
            'data': TransactionSerializer(transaction).data
        })


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Categories."""
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        org_id = self.request.query_params.get('organization_id')
        
        # Get system categories + organization custom categories
        qs = Category.objects.filter(is_active=True, parent__isnull=True)
        
        if org_id:
            qs = qs.filter(organization_id__in=[None, org_id])
        else:
            qs = qs.filter(organization__isnull=True)
        
        return qs.prefetch_related('subcategories').order_by('sort_order', 'name')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Group by type
        income = self.get_serializer(queryset.filter(category_type='income'), many=True).data
        expense = self.get_serializer(queryset.filter(category_type='expense'), many=True).data
        
        return Response({
            'success': True,
            'data': {
                'income': income,
                'expense': expense
            }
        })
