"""
Account URL Configuration
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, MeView,
    PasswordChangeView, OTPSendView, OTPVerifyView
)

urlpatterns = [
    # Authentication
    path('register', RegisterView.as_view(), name='auth-register'),
    path('login', LoginView.as_view(), name='auth-login'),
    path('logout', LogoutView.as_view(), name='auth-logout'),
    path('refresh', TokenRefreshView.as_view(), name='auth-refresh'),
    
    # Profile
    path('me', MeView.as_view(), name='auth-me'),
    
    # Password
    path('password/change', PasswordChangeView.as_view(), name='auth-password-change'),
    
    # OTP
    path('otp/send', OTPSendView.as_view(), name='auth-otp-send'),
    path('otp/verify', OTPVerifyView.as_view(), name='auth-otp-verify'),
]
