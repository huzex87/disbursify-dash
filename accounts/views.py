"""
Account Views - Authentication API
"""
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPCode
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    PasswordChangeSerializer, PasswordResetRequestSerializer,
    PasswordResetSerializer, OTPRequestSerializer, OTPVerifySerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /auth/register
    Create a new user account.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'success': True,
            'data': {
                'user': UserSerializer(user).data,
                'verification_required': {
                    'phone': not user.phone_verified,
                    'email': not user.email_verified
                }
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """
    POST /auth/login
    Authenticate and receive tokens.
    """
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # Record failed login if user exists
            email = request.data.get('email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    user.record_failed_login()
                except User.DoesNotExist:
                    pass
            raise
        
        data = serializer.validated_data
        
        # Get user's organizations
        from organizations.models import Organization, TeamMember
        user = serializer.user
        
        owned_orgs = Organization.objects.filter(owner=user, deleted_at__isnull=True)
        member_orgs = TeamMember.objects.filter(
            user=user, 
            status='active'
        ).select_related('organization')
        
        organizations = []
        for org in owned_orgs:
            organizations.append({
                'id': str(org.id),
                'name': org.name,
                'role': 'owner'
            })
        for tm in member_orgs:
            if tm.organization not in owned_orgs:
                organizations.append({
                    'id': str(tm.organization.id),
                    'name': tm.organization.name,
                    'role': tm.role
                })
        
        return Response({
            'success': True,
            'data': {
                'access_token': data['access'],
                'refresh_token': data['refresh'],
                'token_type': 'Bearer',
                'expires_in': 900,
                'user': data['user'],
                'organizations': organizations,
                'default_organization_id': str(organizations[0]['id']) if organizations else None
            }
        })


class LogoutView(APIView):
    """
    POST /auth/logout
    Invalidate refresh token.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'success': True,
                'data': {'message': 'Logged out successfully'}
            })
        except Exception:
            return Response({
                'success': True,
                'data': {'message': 'Logged out successfully'}
            })


class RefreshTokenView(TokenRefreshView):
    """
    POST /auth/refresh
    Get new access token.
    """
    pass


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET/PATCH /auth/me
    Get or update current user profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data
        })


class PasswordChangeView(APIView):
    """
    POST /auth/password/change
    Change password for authenticated user.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({
            'success': True,
            'data': {'message': 'Password changed successfully'}
        })


class OTPSendView(APIView):
    """
    POST /auth/otp/send
    Send OTP to phone or email.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone = serializer.validated_data.get('phone')
        email = serializer.validated_data.get('email')
        otp_type = serializer.validated_data['otp_type']
        
        # Generate 6-digit OTP
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Create OTP record
        OTPCode.objects.create(
            phone=phone,
            email=email,
            code=code,
            otp_type=otp_type,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        
        # TODO: Send actual SMS/email via Twilio/SendGrid
        # For development, just log it
        print(f"OTP Code: {code} for {phone or email}")
        
        return Response({
            'success': True,
            'data': {
                'message': f'OTP sent to {phone or email}',
                'expires_in': 300,
                'resend_available_at': (timezone.now() + timedelta(seconds=60)).isoformat()
            }
        })


class OTPVerifyView(APIView):
    """
    POST /auth/otp/verify
    Verify OTP code.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone = serializer.validated_data.get('phone')
        email = serializer.validated_data.get('email')
        code = serializer.validated_data['code']
        
        # Find valid OTP
        otp = OTPCode.objects.filter(
            phone=phone if phone else None,
            email=email if not phone else None,
            code=code,
            is_used=False
        ).order_by('-created_at').first()
        
        if not otp or not otp.is_valid():
            return Response({
                'success': False,
                'error': {
                    'code': 'INVALID_OTP',
                    'message': 'Invalid or expired OTP code'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark as used
        otp.is_used = True
        otp.save()
        
        # If phone verification, update user
        if phone and otp.otp_type == 'phone_verification':
            User.objects.filter(phone=phone).update(
                phone_verified=True,
                phone_verified_at=timezone.now()
            )
        
        return Response({
            'success': True,
            'data': {
                'verified': True,
                'type': otp.otp_type
            }
        })
