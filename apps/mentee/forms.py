from django import forms
from django.contrib.auth.models import User
from apps.user.models import UserProfile

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('gender', 'date_of_birth','contact','college','location','state','country','about' )