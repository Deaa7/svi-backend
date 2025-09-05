from rest_framework import serializers
from .models import DoneExams
from profiles.models import Profile_Teacher

class DoneExamsSerializer(serializers.ModelSerializer):
    """
    Complete serializer for DoneExams model
    Used for full CRUD operations with all model fields
    Provides comprehensive data representation for exam completion records
    """
    class Meta:
        model = DoneExams
        # Include all fields for complete data representation
        fields = '__all__'
 
class GetExamsDone(serializers.ModelSerializer):
    """
    Preview serializer for DoneExams model
    Used for listing exam completion records with essential fields only
    Optimized for displaying exam completion data in lists
    """
    class Meta:
        model = DoneExams
        # Define essential fields for exam completion display
        fields = [
            'subject_name',      # Subject name for categorization
            'exam_name',         # Name/title of the exam
            'exam_id',           # Unique identifier for the exam
            'result',            # Student's exam result/score
            'price',             # Price of the exam
            'time_taken',        # Time taken to complete the exam
            'publisher_id',      # ID of the exam publisher
            'publisher_name',    # Name of the exam publisher
            'date_of_application' # Date when the exam was taken
        ]


class GetSolvedSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for DoneExams model
    Used for retrieving only exam IDs that have been completed
    Optimized for lightweight data transfer when only exam IDs are needed
    """
    class Meta:
        model = DoneExams
        # Include only exam_id for minimal data representation
        fields = ('exam_id',)

############################################################### premium content

 
 