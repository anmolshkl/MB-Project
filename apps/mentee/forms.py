from django import forms
from django.contrib.auth.models import User
from apps.mentee.models import MenteeProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email', 'password','first_name','last_name')

class MenteeProfileForm(forms.ModelForm):
    class Meta:
        model = MenteeProfile
        fields = ('gender', 'date_of_birth','contact','college','location','state','country','about' )
