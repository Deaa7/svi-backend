from rest_framework import serializers
from .models import Notes, NoteImages
from profiles.models import Profile_Teacher

class NoteSerializer(serializers.ModelSerializer):
    """
    Complete serializer for Notes model
    Used for displaying notes with full content
    Includes all essential fields for complete note representation
    """
    class Meta:
        model = Notes
        # Define fields for complete note display including content
        fields = [
            'id',              # Unique note identifier
            'title',           # Note title
            'subject_name',    # Subject name
            'publisher_name',  # Name of the teacher who published the note
            'price',           # Note price
            'content'          # Full note content
        ]


class NoteImagesSerializer(serializers.ModelSerializer):
    """
    Complete serializer for NoteImages model
    Used for handling note image uploads and retrieval
    Includes all fields for complete image management
    """
    class Meta:
        model = NoteImages
        # Include all fields for complete image data representation
        fields = '__all__'


class NoteFilterSerializer(serializers.ModelSerializer):
    """
    Preview serializer for Notes model
    Used for listing notes without content for preview purposes
    Optimized for displaying note information in lists and search results
    """
    class Meta:
        model = Notes
        # Define essential fields for note preview (excluding content)
        fields = [
            'id',                    # Unique note identifier
            'title',                 # Note title
            'publisher_name',        # Name of the teacher who published the note
            'date_uploaded',         # Date when the note was uploaded
            'price',                 # Note price
            'number_of_reads',       # Count of times the note has been read
            'number_of_purchases',   # Count of times the note has been purchased
            'publisher_id',          # ID of the teacher who published the note
            'subject_name',          # Subject name
            'Class',                 # Class level (9, 12, or 9_12)
            'number_of_comments'     # Count of comments on the note
        ]


class NoteInfoForEditSerializer(serializers.ModelSerializer):
    """
    Edit serializer for Notes model
    Used for retrieving note information needed for editing
    Includes fields required for note modification while maintaining security
    """
    class Meta:
        model = Notes
        # Define fields needed for note editing
        fields = [
            'id',              # Unique note identifier
            'title',           # Note title
            'publisher_name',  # Name of the teacher who published the note
            'price',           # Note price
            'Class',           # Class level
            'subject_name',    # Subject name
            'content'          # Note content for editing
        ]



