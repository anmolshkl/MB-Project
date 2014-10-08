from django import forms
from django.contrib.auth.models import User
from apps.mentor.models import UserProfile, EducationDetails

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email', 'password','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender', 'date_of_birth','contact','address','country','location','about' )

class EducationForm(forms.ModelForm):
	class Meta:
		model = EducationDetails
		fields = ('institution', 'location', 'degree', 'branch', 'from_year', 'to_year', 'country')