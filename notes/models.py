from django.db import models
from profiles.models import Profile_Teacher

class Notes(models.Model):
    """
    Model to store educational notes published by teachers
    Contains note content, metadata, pricing, and usage statistics
    Each note is associated with a specific teacher and subject
    """
    
    # Note title and identification
    title = models.CharField(max_length=2000)
    
    # Academic information
    subject_name = models.CharField(max_length=25, default='math_12', blank=True)
    Class = models.CharField(max_length=25, default='12', blank=True)
    
    # Publisher information
    publisher_id = models.BigIntegerField(default=1, blank=True)
    publisher_name = models.CharField(max_length=127, default='SVI', blank=True)
    
    # Timestamp
    date_uploaded = models.DateTimeField(auto_now_add=True)
    
    # Note content
    content = models.TextField(blank=False)
    
    # Pricing information
    price = models.IntegerField(default=0, blank=True)
    
    # Usage statistics (auto-managed)
    number_of_reads = models.IntegerField(
        verbose_name='number of reads', 
        default=0, 
        editable=False, 
        null=True, 
        blank=True
    )
    number_of_purchases = models.IntegerField(default=0, editable=False)
    number_of_comments = models.IntegerField(default=0, blank=True)
    
    class Meta:
        """
        Meta configuration for the Notes model
        Defines model behavior and display settings
        """
        # Order records by date uploaded (newest first)
        ordering = ['-date_uploaded']
    
    def __str__(self):
        """
        String representation of the note
        Returns the note title for easy identification
        """
        return self.title
    
    @property 
    def get_publisher_full_name(self):
        """
        Property to get the full name of the teacher who published the note
        Retrieves teacher information from Profile_Teacher model
        """
        obj = Profile_Teacher.objects.get(user_id=self.publisher_id)
        return obj.first_name + ' ' + obj.last_name


class NoteImages(models.Model):
    """
    Model to store images associated with notes
    Allows attaching multiple images to a single note
    Automatically handles image file cleanup when notes are deleted
    """
    
    # Foreign key relationship to the note this image belongs to
    note_id = models.ForeignKey(Notes, on_delete=models.CASCADE)
    
    # The actual image file
    # Uploads to "ImagesForNotes/" directory
    images = models.ImageField(
        upload_to="ImagesForNotes/", 
        verbose_name='إضافة صورة',  # Add image
        null=True, 
        blank=True
    )
