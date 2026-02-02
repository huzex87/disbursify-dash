"""
Transaction URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, CategoryViewSet

router = DefaultRouter()
router.register('transactions', TransactionViewSet, basename='transactions')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]
