from django.db import models
from profiles.models import Profile_Student
from notes.models import Notes

# Create your models here.

class StudentReadNotes(models.Model):
    """
    Model to track when a student reads a note
    Records detailed information about student reading behavior including
    read counts, timestamps, and relationships to notes and publishers
    """
    
    # Foreign key relationship to the student who read the note
    student = models.ForeignKey(
        Profile_Student, 
        on_delete=models.CASCADE, 
        verbose_name='Student',
        related_name='read_notes',
        help_text="Reference to the student who read this note"
    )
    
    # Subject name for categorizing the note
    subject_name = models.CharField(
        max_length=25, 
        verbose_name='Subject Name',
        help_text='Name of the subject associated with the note'
    )
    
    # Title or name of the note that was read
    note_name = models.CharField(
        max_length=2000, 
        verbose_name='Note Name',
        help_text='Title or name of the note'
    )
    
    # Foreign key relationship to the actual note that was read
    note_id = models.ForeignKey(
        Notes, 
        on_delete=models.CASCADE, 
        verbose_name='Note',
        related_name='student_reads',
        help_text="Reference to the note that was read"
    )
    
    # ID of the teacher who published the note
    publisher_id = models.BigIntegerField(
        verbose_name='Publisher ID',
        help_text='ID of the note publisher'
    )
    
    # Name of the teacher who published the note
    publisher_name = models.CharField(
        max_length=127, 
        verbose_name='Publisher Name',
        help_text='Name of the note publisher'
    )
    
    # Counter for tracking how many times the student has read this note
    number_of_reads = models.IntegerField(
        default=1, 
        verbose_name='Number of Reads',
        help_text='Number of times this note has been read by this student'
    )
    
    # Timestamp of when the student first read this note
    first_read_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='First Read At',
        help_text='Timestamp of when the student first read this note'
    )
    
    # Timestamp of when the student last read this note (auto-updates)
    last_read_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Last Read At',
        help_text='Timestamp of when the student last read this note'
    )

    class Meta:
        """
        Meta configuration for the StudentReadNotes model
        Defines model behavior, constraints, and display settings
        """
        # Human-readable names for admin interface
        verbose_name = 'Student Read Note'
        verbose_name_plural = 'Student Read Notes'
        
        # Ensure unique combination of student and note
        # Prevents duplicate read records for the same student-note combination
        unique_together = ['student', 'note_id']
        
        # Default ordering by last read time (most recent first)
        ordering = ['-last_read_at']

    def __str__(self):
        """
        String representation of the model instance
        Returns: Student name - Note name (Subject name) for easy identification
        """
        return f"{self.student.full_name} - {self.note_name} ({self.subject_name})"

    def increment_reads(self):
        """
        Increment the number of reads for this note by this student
        Updates both the read count and the last read timestamp
        Uses update_fields for efficient database updates
        """
        self.number_of_reads += 1
        self.save(update_fields=['number_of_reads', 'last_read_at'])
