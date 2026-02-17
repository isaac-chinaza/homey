from django.contrib import admin
from .models import Property, Unit

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'owner', 'manager', 'status')
    list_filter = ('property_type', 'status')
    search_fields = ('name', 'address')
    inlines = [UnitInline]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('property', 'unit_number', 'rent_amount', 'is_occupied')
    list_filter = ('is_occupied',)
