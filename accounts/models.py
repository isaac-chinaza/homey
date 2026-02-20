from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from decouple import config



cloudinary.config( 
    cloud_name = config("CLOUDINARY_CLOUD_NAME"), 
    api_key = config("CLOUDINARY_API_KEY"), 
    api_secret = config("CLOUDINARY_API_SECRET"), # Click 'View API Keys' above to copy your API secret
    secure=True
)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")


        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('owner', 'Property Owner'),
        ('manager', 'Property Manager'),
        ('tenant', 'Tenant'),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = CloudinaryField('image', folder='profile_pics', null=True, blank=True)
    USERNAME_FIELD = "email"
    objects = UserManager()
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    class Meta:
        ordering = ["email"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"

    @property
    def is_owner(self):
        return self.role == 'owner'
        
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_tenant(self):
        return self.role == 'tenant'
