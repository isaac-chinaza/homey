from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Role'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Profile Picture'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role", "phone_number", "profile_picture")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Password placeholders (UserCreationForm fields)
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Password",
            "class": "form-control"
        })
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirm password",
            "class": "form-control"
        })

