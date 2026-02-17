from accounts.models import User
from django.db import models


class Property(models.Model):
    PROPERTY_TYPES = (
        ('apartment', 'Apartment'),
        ('duplex', 'Duplex'),
        ('commercial', 'Commercial'),
        ('house', 'House'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    )

    name = models.CharField(max_length=255)
    address = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    number_of_units = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_properties', limit_choices_to={'role': 'owner'})
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_properties', limit_choices_to={'role': 'manager'})
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Properties"

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=20)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.property.name} - Unit {self.unit_number}"
