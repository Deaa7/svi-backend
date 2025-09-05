from django.db import models
from django.dispatch import receiver 
from users.models import User
from django.db.models.signals import post_save

# Create your models here.

class Profile_Student(models.Model):
    """
    Model to store student profile information
    Contains personal details, academic information, and financial balance
    Automatically created when a new non-teacher user is registered
    """
    
    # One-to-one relationship with User model (primary key)
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    
    # Personal information fields
    full_name = models.CharField(max_length=127, default="", blank=True)
    city = models.CharField(max_length=50, default="", blank=True)
    school = models.CharField(max_length=200, default="-", blank=True)
    phone_number = models.CharField(max_length=15, default="-", blank=True)
    
    # Academic information
    Class = models.CharField(max_length=2, default='12', blank=True)
    
    # Financial information
    balance = models.IntegerField(default=0)
    
    # Personal details
    gender = models.CharField(max_length=1, default="M")
    
    def __str__(self):
        """
        String representation of the student profile
        Returns the associated user for easy identification
        """
        return str(self.user)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create student profile when a new user is created
    Only creates profile for non-teacher users
    """
    user = instance
 
    # Create student profile only for new non-teacher users
    if created and not user.is_teacher:
        profile = Profile_Student(user=user)
        profile.save()


class Profile_Teacher(models.Model):
    """
    Model to store teacher profile information
    Contains personal details, teaching information, contact details, and statistics
    Automatically created when a new teacher user is registered
    """
    
    # Choices for class levels (in Arabic)
    class_choices = [
        ('12', 'بكلوريا'),      # Baccalaureate
        ('9', 'تاسع'),          # 9th Grade
        ('9_12', 'تاسع و بكلوريا')  # Both 9th Grade and Baccalaureate
    ]
    
    # Choices for subjects (in Arabic)
    subject_choices = [
        ('math', 'رياضيات'),              # Mathematics
        ('physics', 'فيزياء'),            # Physics
        ('chemistry', 'كيمياء'),          # Chemistry
        ('science', 'علوم'),              # Science
        ('arabic', 'عربي'),               # Arabic
        ('english', 'إنكليزي'),           # English
        ('france', 'فرنسي'),              # French
        ('islam', 'ديانة'),               # Islamic Studies
        ('physics_chemistry', 'فيزياء و كيمياء'),  # Physics and Chemistry
        ('geography', 'اجتماعيات'),       # Social Studies
    ]

    # One-to-one relationship with User model (primary key)
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    
    # Personal information
    full_name = models.CharField(max_length=127, default="", blank=True)
    
    # Teaching information
    studying_subjects = models.CharField(max_length=100, choices=subject_choices)
    
    # Profile image
    image = models.ImageField(
        upload_to="TeachersImages/", 
        verbose_name='إضافة صورة',  # Add image
        null=True, 
        blank=True
    )
    
    # Biography and description
    bio = models.CharField(default='', max_length=5000, blank=True, null=True)
    
    # Financial information
    total_net = models.IntegerField(default=0, blank=True)
    
    # Timestamp
    created_at = models.DateField(auto_now_add=True)
    
    # Location and academic information
    city = models.CharField(max_length=50, default="", blank=True)
    Class = models.CharField(max_length=15, choices=class_choices, blank=True, default='12')
    gender = models.CharField(default='M', max_length=1)
    
    # Teaching experience
    teaching_in_school = models.CharField(default='', max_length=255, blank=True, null=True)
    teaching_in_institutions = models.CharField(default='', max_length=500, blank=True, null=True)
    
    # Statistics
    number_of_exams = models.IntegerField(default=0, blank=True)
    number_of_notes = models.IntegerField(default=0, blank=True)
    
    # Contact information section
    phone_number = models.CharField(max_length=15, default='-', blank=True)
    another_phone_number = models.CharField(max_length=15, default='-', blank=True)
    telegram_link = models.CharField(default='', max_length=500, blank=True, null=True)
    whatsapp_link = models.CharField(default='', max_length=500, blank=True, null=True)
    facebook_link = models.CharField(default='', max_length=500, blank=True, null=True)
    instagram_link = models.CharField(default='', max_length=500, blank=True, null=True)
    
    def __str__(self):
        """
        String representation of the teacher profile
        Returns the teacher's full name for easy identification
        """
        return self.full_name


@receiver(post_save, sender=User)
def save_profile_teacher(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create teacher profile when a new teacher user is created
    Only creates profile for new teacher users
    """
    user = instance

    # Create teacher profile only for new teacher users
    if created and user.is_teacher:
        profile = Profile_Teacher(user=user)
        profile.save()

 