"""
Account Serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""
    
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone', 'first_name', 'last_name', 'full_name',
            'avatar_url', 'timezone', 'locale', 'email_verified', 'phone_verified',
            'two_factor_enabled', 'date_joined', 'last_login_at'
        ]
        read_only_fields = ['id', 'email', 'email_verified', 'phone_verified', 'date_joined', 'last_login_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'phone', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """Custom login serializer with additional user data."""
    
    remember_me = serializers.BooleanField(default=False, required=False)
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        data['user'] = UserSerializer(self.user).data
        
        # Record login
        request = self.context.get('request')
        ip = request.META.get('REMOTE_ADDR') if request else None
        self.user.record_login(ip)
        
        return data


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request."""
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset."""
    token = serializers.CharField()
    password = serializers.CharField(validators=[validate_password])


class OTPRequestSerializer(serializers.Serializer):
    """Serializer for OTP request."""
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    otp_type = serializers.ChoiceField(choices=['phone_verification', 'password_reset'])


class OTPVerifySerializer(serializers.Serializer):
    """Serializer for OTP verification."""
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    code = serializers.CharField(max_length=6)
