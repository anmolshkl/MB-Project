from django import forms
from django.contrib.auth.models import User
from apps.user.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender', 'date_of_birth', 'contact', 'college', 'city', 'state', 'country', 'about', 'picture')
        widgets = {
            'about': forms.Textarea(attrs={'rows': 2}),
            'contact': forms.TextInput(attrs={'placeholder': 'eg +91 9970631445'}),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}, format="%m/%d/%Y"),
            'city': forms.TextInput(attrs={'placeholder': 'Mumbai'}),
            'country': forms.TextInput(attrs={'placeholder': 'India'}),
            'state': forms.TextInput(attrs={'placeholder': 'Maharashtra'})
        }
