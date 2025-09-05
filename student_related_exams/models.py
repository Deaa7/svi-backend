from django.db import models
from profiles.models import Profile_Student

# Create your models here.

class DoneExams(models.Model):
    """
    Model to track exams completed by students
    Records comprehensive information about exam completion including
    student details, exam information, results, timing, and publisher data
    """
    
    # Foreign key relationship to the student who completed the exam
    student = models.ForeignKey(
        Profile_Student, 
        on_delete=models.CASCADE,
        help_text="Reference to the student who completed this exam"
    )
    
    # Subject name for categorizing the exam
    subject_name = models.CharField(
        max_length=25,
        help_text="Name of the subject for this exam"
    )
    
    # Name or title of the specific exam
    exam_name = models.CharField(
        max_length=100,
        help_text="Name or title of the exam"
    )
    
    # Unique identifier for the exam (same as package ID)
    exam_id = models.CharField(
        max_length=50,
        help_text="Unique identifier for the exam (same as package ID)"
    )
    
    # ID of the teacher who published the exam
    publisher_id = models.IntegerField(
        default=1,
        help_text="ID of the teacher who published this exam"
    )
    
    # Name of the teacher who published the exam
    publisher_name = models.CharField(
        max_length=127, 
        default='SVI', 
        blank=True,
        help_text="Name of the teacher who published this exam"
    )
    
    # Date when the student took the exam
    date_of_application = models.DateField(
        auto_now_add=True,
        blank=True,
        help_text="Date when the student took this exam"
    )
    
    # Student's result/score on the exam
    result = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Student's result/score on this exam"
    )
    
    # Price of the exam
    price = models.IntegerField(
        default=0,
        help_text="Price of the exam"
    )
    
    # Time taken by the student to complete the exam
    time_taken = models.TimeField(
        default='00:00:00', 
        blank=True,
        help_text="Time taken by the student to complete this exam"
    )

    class Meta:
        """
        Meta configuration for the DoneExams model
        Defines model behavior and display settings
        """
        # Order records by date of application (newest first)
        ordering = ['-date_of_application']


