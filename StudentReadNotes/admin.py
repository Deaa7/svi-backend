from django.contrib import admin
from .models import StudentReadNotes

@admin.register(StudentReadNotes)
class StudentReadNotesAdmin(admin.ModelAdmin):
    """
    Admin interface for StudentReadNotes model
    Provides comprehensive management interface for student reading tracking data
    Includes filtering, searching, and organized field display for reading analytics
    """
    
    # List display configuration - fields shown in the list view
    list_display = [
        'student', 'note_name', 'subject_name', 'publisher_name', 
        'number_of_reads', 'first_read_at', 'last_read_at'
    ]
    
    # List filters - sidebar filters for quick filtering
    list_filter = [
        'subject_name',      # Filter by subject
        'publisher_name',    # Filter by publisher/teacher
        'first_read_at',     # Filter by first read date
        'last_read_at'       # Filter by last read date
    ]
    
    # Search functionality - fields that can be searched
    search_fields = [
        'student__full_name',  # Search by student's full name
        'note_name',           # Search by note name/title
        'publisher_name'       # Search by publisher name
    ]
    
    # Read-only fields that cannot be edited
    readonly_fields = [
        'first_read_at',  # First read timestamp (auto-generated)
        'last_read_at'    # Last read timestamp (auto-updated)
    ]
    
    # Default ordering of records (most recent reads first)
    ordering = ['-last_read_at']
    
    # Fieldsets - organize fields into logical groups in the edit form
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'subject_name'),
            'description': 'Student and subject information for the reading record'
        }),
        ('Note Information', {
            'fields': ('note_name', 'note_id', 'publisher_id', 'publisher_name'),
            'description': 'Details about the note that was read and its publisher'
        }),
        ('Read Statistics', {
            'fields': ('number_of_reads', 'first_read_at', 'last_read_at'),
            'description': 'Reading statistics including read count and timestamps'
        }),
    )
