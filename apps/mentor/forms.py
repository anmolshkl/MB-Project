from django import forms
from django.contrib.auth.models import User
from apps.user.models import UserProfile
from apps.mentor.models import EducationDetails, EmploymentDetails
from django.forms.models import inlineformset_factory


class EmploymentForm(forms.ModelForm):
	class Meta:
		model = EmploymentDetails
		fields = ('organization','location','position','from_date','to_date')

class EducationForm(forms.ModelForm):
	class Meta:
		model = EducationDetails
		fields = ('institution', 'location', 'degree', 'branch', 'from_year', 'to_year', 'country')

class UserProfileForm(forms.ModelForm):
	
	class Meta:
		model = UserProfile
		fields = ('gender', 'date_of_birth','contact','location','country','about','picture')

EducationDetailsFormSet  = inlineformset_factory(UserProfile, EducationDetails,
                                                form=EducationForm, extra=0, can_delete=False)
EmploymentDetailsFormSet = inlineformset_factory(UserProfile, EmploymentDetails,
                                                form=EmploymentForm, extra=0, can_delete=False)

