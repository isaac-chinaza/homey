from django import forms
from .models import Tenant
from accounts.models import User
from properties.models import Unit

class TenantForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='tenant', tenant_profile__isnull=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select a user registered as a tenant who is not yet assigned."
    )
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.filter(is_occupied=False),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    class Meta:
        model = Tenant
        fields = ['user', 'unit', 'lease_start_date', 'lease_end_date', 'lease_document']
        widgets = {
            'lease_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lease_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lease_document': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ContactManagerForm(forms.Form):
    subject = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is this about?'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Type your message here...'})
    )
