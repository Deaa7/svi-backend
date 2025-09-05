from django.contrib import admin
from .models import StudentSubjectTracking

@admin.register(StudentSubjectTracking)
class StudentSubjectTrackingAdmin(admin.ModelAdmin):
    """
    Admin interface for StudentSubjectTracking model
    Provides comprehensive management interface for student subject tracking data
    Includes filtering, searching, and organized field display
    """
    
    # List display configuration - fields shown in the list view
    list_display = [
        'student', 
        'subject_name', 
        'Class', 
        'number_of_notes', 
        'number_of_exams'
    ]
    
    # List filters - sidebar filters for quick filtering
    list_filter = [
        'subject_name',
        'Class'
    ]
    
    # Search functionality - fields that can be searched
    search_fields = [
        'student__username',  # Search by student username
        'student__email',     # Search by student email
        'subject_name'        # Search by subject name
    ]
    
    # Fieldsets - organize fields into logical groups in the edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'subject_name', 'Class'),
            'description': 'Essential student and subject information'
        }),
        ('Content Counts', {
            'fields': ('number_of_notes', 'number_of_exams'),
            'description': 'Progress tracking counters for notes and exams'
        }),
    )
    
    # Number of items displayed per page in the list view
    list_per_page = 25
    
    # Default ordering of records (newest first)
    ordering = ['-id']
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related for better performance
        Reduces database queries by prefetching related student data
        """
        return super().get_queryset(request).select_related('student')
