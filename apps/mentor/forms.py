from django import forms
from django.contrib.auth.models import User
from apps.mentor.models import MentorProfile, EducationDetails

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('pictures', 'gender', 'date_of_birth','location','short_bio', )

class EducationForm(forms.ModelForm):
	class Meta:
		model = EducationDetails
		fields = ('institution', 'location', 'degree', 'branch', 'from_year', 'to_year', 'country')