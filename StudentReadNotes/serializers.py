from rest_framework import serializers
from .models import StudentReadNotes

class StudentReadNotesSerializer(serializers.ModelSerializer):
    """Serializer for StudentReadNotes model"""
    student_full_name = serializers.CharField(source='student.full_name', read_only=True)
    note_title = serializers.CharField(source='note_id.title', read_only=True)
    
    class Meta:
        model = StudentReadNotes
        fields = [
            'id', 'student', 'student_full_name', 'subject_name', 'note_name', 
            'note_id', 'publisher_id', 'publisher_name', 'number_of_reads',
            'first_read_at', 'last_read_at', 'note_title'
        ]
        read_only_fields = ['id', 'first_read_at', 'last_read_at', 'student_full_name', 'note_title']

class CreateStudentReadNotesSerializer(serializers.ModelSerializer):
    """Serializer for creating StudentReadNotes instances"""
    
    class Meta:
        model = StudentReadNotes
        fields = [
            'student', 'subject_name', 'note_name', 'note_id', 
            'publisher_id', 'publisher_name'
        ]

class StudentReadNotesPreviewSerializer(serializers.ModelSerializer):
    """Serializer for preview/list view without full note content"""
    student_full_name = serializers.CharField(source='student.full_name', read_only=True)
    note_title = serializers.CharField(source='note_id.title', read_only=True)
    
    class Meta:
        model = StudentReadNotes
        fields = [
            'id', 'student_full_name', 'subject_name', 'note_name', 
            'note_id', 'publisher_id', 'publisher_name', 'number_of_reads',
            'first_read_at', 'last_read_at', 'note_title'
        ]
