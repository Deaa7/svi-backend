from rest_framework import serializers
from .models import User

class SingUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    Handles validation and serialization of user registration data
    Used for creating new user accounts during the registration process
    """
    class Meta:
        model = User
        # Define fields required for user registration
        fields = ('username', 'email', 'password', 'is_teacher')
    
    def validate_username(self, value):
        """
        Custom validation for username field
        Ensures username meets minimum requirements and is unique
        """
        if len(value) < 3:
            raise serializers.ValidationError("اسم المستخدم يجب أن يكون 3 أحرف على الأقل")
        return value
    
    def validate_email(self, value):
        """
        Custom validation for email field
        Ensures email format is valid and unique
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("هذا البريد الإلكتروني مسجل بالفعل")
        return value
    
    def validate_password(self, value):
        """
        Custom validation for password field
        Ensures password meets security requirements
        """
        if len(value) < 6:
            raise serializers.ValidationError("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
        return value

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data display
    Used for returning user information in API responses
    Excludes sensitive fields like password for security
    """
    class Meta:
        model = User
        # Define fields to be included in user data responses
        # Excludes password for security reasons
        fields = ('id', 'username', 'email', 'is_teacher') 