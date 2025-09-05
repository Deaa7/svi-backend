from rest_framework import serializers
from .models import Profile_Teacher, Profile_Student
from users.models import User
from notes.models import Notes
from django.db import connection
from test_packages.models import TestPackage

class ProfileTeacherSerializer(serializers.ModelSerializer):
    """
    Complete serializer for Profile_Teacher model
    Used for full CRUD operations with all model fields
    Provides comprehensive data representation for teacher profiles
    """
    class Meta:
        model = Profile_Teacher 
        # Include all fields for complete data representation
        fields = '__all__'


class TeacherPreviewSerializer(serializers.ModelSerializer):
    """
    Preview serializer for Profile_Teacher model
    Used for listing teachers with essential fields only
    Optimized for displaying teacher information in lists and search results
    """
    class Meta:
        model = Profile_Teacher 
        # Define essential fields for teacher preview display
        fields = [
            'user_id',           # User ID for identification
            'full_name',         # Teacher's full name
            'studying_subjects', # Subjects the teacher teaches
            'city',              # Teacher's city
            'Class',             # Classes the teacher teaches
            'gender',            # Teacher's gender
            'number_of_notes',   # Count of notes published
            'number_of_exams',   # Count of exams published
            'image'              # Teacher's profile image
        ]


################################################################ student section 

class StudentOwnProfile(serializers.ModelSerializer):
    """
    Complete serializer for Profile_Student model
    Used for retrieving student's own profile information
    Provides comprehensive data representation for student profiles
    """
    class Meta:
        model = Profile_Student 
        # Include all fields for complete student profile data
        fields = '__all__'


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Update serializer for Profile_Student model
    Used for updating student profile information with validation
    Includes custom validation for Class and gender fields
    """
    class Meta:
        model = Profile_Student
        # Define fields that can be updated by students
        fields = [
            'full_name',     # Student's full name
            'city',          # Student's city
            'school',        # Student's school
            'phone_number',  # Student's phone number
            'Class',         # Student's class (9 or 12)
            'gender'         # Student's gender (M or F)
        ]
    
    def validate_Class(self, value):
        """
        Custom validation for Class field
        Ensures Class is either '9' or '12' as per system requirements
        """
        if value not in ['9', '12']:
            raise serializers.ValidationError("الفصل يجب أن يكون إما '9' أو '12'")
        return value
    
    def validate_gender(self, value):
        """
        Custom validation for gender field
        Ensures gender is either 'M' (Male) or 'F' (Female)
        """
        if value not in ['M', 'F']:
            raise serializers.ValidationError("الجنس يجب أن يكون إما 'M' أو 'F'")
        return value