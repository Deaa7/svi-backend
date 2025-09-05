from django.db import models
from users.models import User
from profiles.models import Profile_Student

# Create your models here.

class StudentSubjectTracking(models.Model):
    """
    Model to track student progress and engagement with subjects
    Records the number of notes and exams completed by each student for each subject and class
    Provides insights into student learning patterns and subject engagement
    """
    
    # Foreign key relationship to the student user
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='subject_tracking',
        verbose_name='Student ID (FK)',
        help_text="Reference to the student user who is being tracked"
    )
    
    # Class/grade level for the subject tracking
    Class = models.CharField(
        max_length=2, 
        default='12',
        verbose_name='Class',
        help_text="Class (e.g., '9', '12', '9_12')"
    )
    
    # Subject name for tracking specific subjects
    subject_name = models.CharField(
        max_length=25,
        verbose_name='Subject Name',
        help_text="Name of the subject being tracked (e.g., 'math', 'physics', 'chemistry')"
    )
    
    # Counter for number of notes completed by the student
    number_of_notes = models.IntegerField(
        default=0,
        verbose_name='Number of Notes',
        help_text="Total number of notes completed by the student for this subject"
    )
    
    # Counter for number of exams completed by the student
    number_of_exams = models.IntegerField(
        default=0,
        verbose_name='Number of Exams',
        help_text="Total number of exams completed by the student for this subject"
    )
    
    class Meta:
        """
        Meta configuration for the StudentSubjectTracking model
        Defines model behavior, constraints, and display settings
        """
        # Human-readable names for admin interface
        verbose_name = 'Student Subject Tracking'
        verbose_name_plural = 'Student Subject Tracking'
        
        # Ensure unique combination of student, subject, and class
        # Prevents duplicate tracking records for the same student-subject-class combination
        unique_together = ['student', 'subject_name', 'Class']
        
        # Default ordering by ID (newest first)
        ordering = ['-id']
    
    def __str__(self):
        """
        String representation of the model instance
        Returns: Student username - Subject name (Class) for easy identification
        """
        return f"{self.student.username} - {self.subject_name} ({self.Class})"
