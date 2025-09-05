from rest_framework import serializers
from .models import StudentPremiumContent
from profiles.models import Profile_Student
from notes.models import Notes


class StudentPremiumContentSerializer(serializers.ModelSerializer):
    """
    Full serializer for StudentPremiumContent with all fields
    This serializer provides complete data representation including computed fields
    """
    # Computed fields that get data from related student profile
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    
    class Meta:
        model = StudentPremiumContent
        # Define all fields to be included in serialization
        fields = [
            'id', 'student', 'student_name', 'student_email', 'Class', 'type',
            'subject_name', 'content_id', 'content_name', 'publisher_id',
            'publisher_name', 'purchase_date', 'price', 'date_of_expiry'
        ]
        # Fields that cannot be modified through the API
        read_only_fields = ['id', 'purchase_date', 'student_name', 'student_email']


class StudentPremiumContentPreviewSerializer(serializers.ModelSerializer):
    """
    Preview serializer for StudentPremiumContent with all fields
    Used for list views where full data is needed but without computed fields
    """
    class Meta:
        model = StudentPremiumContent
        # Include all model fields in serialization
        fields = '__all__'


class CreateStudentPremiumContentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating StudentPremiumContent instances
    This serializer handles the creation of new premium content records
    with validation to prevent duplicate purchases
    """
    class Meta:
        model = StudentPremiumContent
        # Define fields required for creating a new premium content record
        fields = [
            'student', 'Class', 'type', 'subject_name', 'content_id',
            'content_name', 'publisher_id', 'publisher_name',
            'price', 'date_of_expiry'
        ]
    
    def validate(self, data):
        """
        Custom validation to ensure unique student-content combinations
        Prevents duplicate premium content purchases for the same student and content
        """
        # Extract student and content_id from the data
        student = data.get('student')
        content_id = data.get('content_id')
        type = data.get('content_type')
        
        # Check if this student already has premium access to this content
        if StudentPremiumContent.objects.filter(student=student, content_id=content_id , type = type).exists():
            raise serializers.ValidationError(
                "هذا الطالب لديه بالفعل وصول مميز لهذا المحتوى."
            )
        
        return data


class StudentPremiumContentFilterSerializer(serializers.ModelSerializer):
    """
    Serializer for filtering StudentPremiumContent with basic fields
    Used for filtered list views with additional computed fields like expiration status
    """
    # Computed field to get student's full name
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    # Computed field to check if content has expired
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentPremiumContent
        # Define fields for filtered/preview display
        fields = [
            'id', 'student_name', 'Class', 'subject_name', 'content_name',
            'publisher_name', 'purchase_date', 'price', 'is_expired'
        ]
    
    def get_is_expired(self, obj):
        """
        Method to check if the premium content has expired
        Compares the expiry date with current time
        """
        from django.utils import timezone
        return obj.date_of_expiry < timezone.now()
