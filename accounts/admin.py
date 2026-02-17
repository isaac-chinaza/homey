from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from .models import User

admin.site.unregister(Group)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['get_full_name', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)
