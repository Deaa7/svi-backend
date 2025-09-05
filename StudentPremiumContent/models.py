from django.db import models
from profiles.models import Profile_Student
from notes.models import Notes
from profiles.models import Profile_Teacher

# Create your models here.

class StudentPremiumContent(models.Model):
    """
    Model to track when a student purchases and accesses premium content
    This model stores information about premium content purchases including
    student details, content information, pricing, and expiration dates
    """
    # Foreign key relationship to the student who purchased the content
    student = models.ForeignKey(
        Profile_Student, 
        on_delete=models.DO_NOTHING, 
        verbose_name='Student',
        related_name='premium_content'
    )
    # Name of the student who purchased the premium content
    student_name = models.CharField(
        max_length=256,
        default="",
        verbose_name='Student Name',
        help_text='Name of the student who purchased the premium content'
    )
    # Class/grade level associated with the premium content
    Class = models.CharField(
        max_length=25, 
        verbose_name='Class',
        help_text='Name of the class associated with the premium content'
    )
    
    # Type of premium content (e.g., 'exam', 'note')
    type = models.CharField(
        max_length=25, 
        verbose_name='Type',
        help_text='Type of the premium content'
    )
    
    # Subject name for the premium content
    subject_name = models.CharField(
        max_length=25, 
        verbose_name='Subject Name',
        help_text='Name of the subject associated with the premium content'
    )
    
    # Unique identifier for the specific content item
    content_id = models.BigIntegerField(
        verbose_name='Content ID',
        help_text='ID of the content'
    )
    
    # Title or name of the premium content
    content_name = models.CharField(
        max_length=2000, 
        verbose_name='Content Name',
        help_text='Title or name of the content'
    )
    
    # Foreign key relationship to the teacher who published the content
    publisher_id = models.ForeignKey(
        Profile_Teacher,
        on_delete=models.DO_NOTHING,
        verbose_name='Publisher ID',
        help_text='ID of the note publisher'
    )
    
    # Name of the teacher who published the content
    publisher_name = models.CharField(
        max_length=127, 
        verbose_name='Publisher Name',
        help_text='Name of the note publisher'
    )
    
    # Automatically set timestamp when the purchase is made
    purchase_date = models.DateField(
        auto_now_add=True, 
        verbose_name='Purchase Date',
        help_text='Timestamp of when the student purchased the premium content'
    )
    
    # Price paid for the premium content
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Price',
        help_text='Price of the premium content'
    )
    
    # Date when the premium content access expires
    date_of_expiry = models.DateField(
        verbose_name='Date of Expiry',
        help_text='Date of expiry of the premium content'
    )
    
    # Boolean flag to indicate if the content has expired
    is_expired = models.BooleanField(
        default=False,
        verbose_name='Is Expired',
        help_text='Whether the premium content is expired'
    )

    class Meta:
        # Order records by purchase date (newest first)
        ordering = ['-purchase_date']
        # Human-readable names for admin interface
        verbose_name = 'Student Premium Content'
        verbose_name_plural = 'Student Premium Content'
        # Ensure each student can only purchase the same content once
        unique_together = ['student', 'content_id' , 'type']

    def __str__(self):
        """
        String representation of the model instance
        Returns: Student name - Content name (Subject name)
        """
        return f"{self.student.full_name} - {self.content_name} ({self.subject_name})"
