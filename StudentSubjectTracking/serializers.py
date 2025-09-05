from rest_framework import serializers
from .models import StudentSubjectTracking
from users.models import User

class StudentSubjectTrackingSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentSubjectTracking model
    Handles serialization and validation of student subject tracking data
    Includes computed fields for student information and comprehensive validation
    """
    
    # Computed fields that get data from related student model
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    
    class Meta:
        model = StudentSubjectTracking
        # Define all fields to be included in serialization
        fields = [
            'id',
            'student',
            'student_username',
            'student_email',
            'Class',
            'subject_name',
            'number_of_notes',
            'number_of_exams'
        ]
        # Fields that cannot be modified through the API
        read_only_fields = ['id']
    
    def validate(self, data):
        """
        Custom validation for the StudentSubjectTracking model
        Performs comprehensive validation of all fields including:
        - Student existence verification
        - Class format validation
        - Subject name validation
        - Count value validation
        """
        # Ensure student exists in the database
        if 'student' in data:
            try:
                User.objects.get(id=data['student'].id)
            except User.DoesNotExist:
                raise serializers.ValidationError("الطالب غير موجود")
        
        # Validate Class format - only specific values are allowed
        if 'Class' in data and data['Class'] not in ['9', '12', '9_12']:
            raise serializers.ValidationError("الفصل يجب أن يكون '9' أو '12' أو '9_12'")
        
        # Validate subject_name format against predefined list of valid subjects
        valid_subjects = [
            'math', 'science', 'english', 'arabic', 'physics', 'chemistry',
            'physics_chemistry', 'islam', 'france', 'geography'
        ]
        if 'subject_name' in data and data['subject_name'] not in valid_subjects:
            raise serializers.ValidationError(f"المادة يجب أن تكون واحدة من: {', '.join(valid_subjects)}")
        
        # Ensure non-negative values for note count
        if 'number_of_notes' in data and data['number_of_notes'] < 0:
            raise serializers.ValidationError("عدد الملاحظات لا يمكن أن يكون سالباً")
        
        # Ensure non-negative values for exam count
        if 'number_of_exams' in data and data['number_of_exams'] < 0:
            raise serializers.ValidationError("عدد الاختبارات لا يمكن أن يكون سالباً")
        
        return data
