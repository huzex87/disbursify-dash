"""
Main URL Configuration for Disbursify Dash API
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint."""
    return Response({
        'success': True,
        'data': {
            'status': 'healthy',
            'service': 'Disbursify Dash API',
            'version': '1.0.0'
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root with available endpoints."""
    return Response({
        'success': True,
        'data': {
            'name': 'Disbursify Dash API',
            'version': '1.0.0',
            'tagline': 'One Dashboard. All Your Businesses.',
            'endpoints': {
                'auth': '/api/v1/auth/',
                'organizations': '/api/v1/organizations/',
                'businesses': '/api/v1/businesses/',
                'transactions': '/api/v1/transactions/',
                'categories': '/api/v1/categories/',
                'docs': '/api/docs/',
                'health': '/health'
            }
        }
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health', health_check, name='health-check'),
    
    # API Root
    path('api/', api_root, name='api-root'),
    path('api/v1/', api_root, name='api-v1-root'),
    
    # API v1
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/organizations/', include('organizations.urls')),
    path('api/v1/businesses/', include('businesses.urls')),
    path('api/v1/', include('transactions.urls')),  # transactions and categories
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
