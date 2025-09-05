from django.db import models
from test_packages.models import TestPackage
from django.dispatch import receiver
from django.db.models.signals import post_delete
import os


class Questions(models.Model):
    """
    Model to store questions for test packages
    Contains question content, multiple choice options, correct answer, and explanation
    Each question is associated with a specific test package
    """
    
    # Foreign key relationship to the test package this question belongs to
    package = models.ForeignKey(TestPackage, on_delete=models.CASCADE)
    
    # The main question text/content
    test_content = models.TextField()
    
    # Multiple choice options (A through E)
    # All options are optional and can be left blank
    option_A = models.TextField(null=True, blank=True)
    option_B = models.TextField(null=True, blank=True)
    option_C = models.TextField(null=True, blank=True)
    option_D = models.TextField(null=True, blank=True)
    option_E = models.TextField(null=True, blank=True)
    
    # The correct answer (A, B, C, D, or E)
    right_answer = models.CharField(max_length=5, default='A')
    
    # Explanation for the correct answer
    # Default text in Arabic: "No explanation available"
    explanation = models.TextField(
        help_text='شرح الإجابة الصحيحة',  # Explanation of the correct answer
        default='لا يتوفر شرح للإجابة',  # No explanation available
        null=True, 
        blank=True
    )
    
    def __str__(self):
        """
        String representation of the question
        Returns package name and question ID for easy identification
        """
        return str(self.package) + ' ' + str(self.id)


class QuestionImages(models.Model):
    """
    Model to store images associated with questions
    Allows attaching images to different parts of a question (content, options, explanation)
    Automatically handles image file cleanup when records are deleted
    """
    
    # Choices for which part of the question the image belongs to
    field_name_choices = [
        ('test_content', 'test_content'),  # Image for the main question content
        ('option_A', 'option_A'),          # Image for option A
        ('option_B', 'option_B'),          # Image for option B
        ('option_C', 'option_C'),          # Image for option C
        ('option_D', 'option_D'),          # Image for option D
        ('option_E', 'option_E'),          # Image for option E
        ('explanation', 'explanation'),    # Image for the explanation
    ]
    
    # Foreign key relationship to the question this image belongs to
    test_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    
    # Field indicating which part of the question this image is for
    field_name = models.CharField(
        max_length=100,
        choices=field_name_choices,
        default='test_content',  # Default to question content
        blank=True, 
        null=True
    )
    
    # The actual image file
    # Uploads to "ImagesForQuestions/" directory
    images = models.ImageField(
        upload_to="ImagesForQuestions/", 
        verbose_name='إضافة صورة',  # Add image
        null=True, 
        blank=True
    )


@receiver(post_delete, sender=QuestionImages)
def delete(sender, instance: QuestionImages, **kwargs):
    """
    Signal handler to automatically delete image files when QuestionImages record is deleted
    Prevents orphaned image files from accumulating on the server
    """
    # Check if the instance has an image
    if instance.images:
        # Get the file path of the image
        image_path = instance.images.path
        
        # Check if the file exists on the filesystem
        if os.path.exists(image_path):
            # Remove the file from the filesystem
            os.remove(image_path)