from django.db import models
from accounts.models import User
from properties.models import Property, Unit

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile', limit_choices_to={'role': 'tenant'})     
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_tenants')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenants') # For cases where unit is not specific or single unit property
    
    lease_start_date = models.DateField(null=True, blank=True)
    lease_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    lease_document = models.FileField(upload_to='lease_documents/', blank=True, null=True)

    def __str__(self):
        return f"Tenant: {self.user.username}"
    
    def save(self, *args, **kwargs):
        # If unit is selected, automatically set property
        if self.unit and not self.property:
            self.property = self.unit.property
        super().save(*args, **kwargs)
