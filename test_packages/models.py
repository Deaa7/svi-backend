 
from django.db import models
from django.db import connection
from profiles.models import Profile_Teacher

class TestPackage(models.Model):
    """
    Model to store test package information
    Represents a collection of tests/exams for a specific subject and class level
    Tracks package details, pricing, usage statistics, and publisher information
    """
    
    # Package identification and description
    package_name = models.CharField(
        max_length=500, 
        help_text="هون منحط شو محتوى الاختبار , متل مثلا اختبار في وحدة الأعصاب , وفي وحدة الهرمونات أو شامل"
    )
    
    # Publisher information
    publisher_id = models.BigIntegerField(
        default=1,
        help_text="ID of the teacher who published this test package"
    )
    publisher_name = models.CharField(
        max_length=127, 
        default='SVI', 
        blank=True,
        help_text="Name of the teacher who published this package"
    )
    
    # Package content and structure
    units = models.CharField(
        max_length=1000,
        help_text="Units or topics covered in this test package"
    )
    
    # Educational level information
    Class = models.CharField(
        max_length=2, 
        default='12',
        help_text="Class/grade level for this test package"
    )
    subject_name = models.CharField(
        max_length=25,
        default='math_12', 
        blank=True,
        help_text="Subject name for this test package"
    )
    
    # Pricing information
    price = models.IntegerField(
        default=0, 
        blank=True,
        help_text="Price of the test package in currency units"
    )
    
    # Timestamp information
    date_added = models.DateField(
        auto_now_add=True,
        help_text="Date when the package was added to the system"
    )
    
    # Usage statistics (read-only fields)
    number_of_apps = models.IntegerField(
        verbose_name='number of applications', 
        default=0, 
        blank=True, 
        editable=False,
        help_text="Number of times this package has been accessed"
    )
    number_of_purchases = models.IntegerField(
        default=0, 
        editable=False,
        help_text="Number of times this package has been purchased"
    )
    
    # Content statistics
    number_of_questions = models.IntegerField(
        default=0, 
        blank=True,
        help_text="Total number of questions in this test package"
    )
 
    
    class Meta:
        """
        Meta configuration for the TestPackage model
        """
        # Order records by date added (newest first)
        ordering = ['-date_added']

    def __str__(self):
        """
        String representation of the model instance
        Returns: Package name with ID for easy identification
        """
        return self.package_name + ' , ' + str(self.id)
  
    @property 
    def get_publisher_full_name(self):
        """
        Property to get the full name of the publisher
        Retrieves the teacher's full name from the Profile_Teacher model
        """
        obj = Profile_Teacher.objects.get(user_id=self.publisher_id)
        return obj.full_name 
    