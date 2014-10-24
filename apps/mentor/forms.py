from django import forms
from django.contrib.auth.models import User
from apps.user.models import UserProfile
from apps.mentor.models import EducationDetails

class EducationForm(forms.ModelForm):
	class Meta:
		model = EducationDetails
		fields = ('institution', 'location', 'degree', 'branch', 'from_year', 'to_year', 'country')

class UserProfileForm(forms.ModelForm):
	is_mentor = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
	class Meta:
		model = UserProfile
		fields = ('gender', 'date_of_birth','contact','location','country','about' )