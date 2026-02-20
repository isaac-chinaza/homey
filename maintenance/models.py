from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from accounts.models import User
from properties.models import Property, Unit
from decouple import config


cloudinary.config( 
    cloud_name = config("CLOUDINARY_CLOUD_NAME"), 
    api_key = config("CLOUDINARY_API_KEY"), 
    api_secret = config("CLOUDINARY_API_SECRET"), # Click 'View API Keys' above to copy your API secret
    secure=True
)

class MaintenanceRequest(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maintenance_requests')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_requests')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    photo = CloudinaryField('image', folder='maintenance_photos', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
