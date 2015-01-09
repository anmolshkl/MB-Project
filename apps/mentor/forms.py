from django import forms
from django.contrib.auth.models import User
from apps.user.models import UserProfile
from apps.mentor.models import EducationDetails, EmploymentDetails
from django.forms.models import inlineformset_factory


class EmploymentForm(forms.ModelForm):
	class Meta:
		model = EmploymentDetails
		fields = ('organization','location','position','from_date','to_date')
		widgets = {
            'from_date': forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}),
            'to_date': forms.DateInput(
                attrs={'placeholder': 'MM/DD/YYYY'}),
        }  

class EducationForm(forms.ModelForm):
	class Meta:
		model = EducationDetails
		fields = ('institution', 'location', 'degree', 'branch', 'from_year', 'to_year', 'country')
		widgets = {
            'from_year': forms.DateInput(attrs={'placeholder': '2010'}),
            'to_year': forms.DateInput(
                attrs={'placeholder': '2014'}),
        }  
class UserProfileForm(forms.ModelForm):
	
	class Meta:
		model = UserProfile
		fields = ('gender', 'date_of_birth','contact','location','country','about','picture','resume')
		widgets = {
          'about': forms.Textarea(attrs={'rows':3}),
        }

EducationDetailsFormSet  = inlineformset_factory(UserProfile, EducationDetails,
                                                form=EducationForm, extra=0, can_delete=True)
EmploymentDetailsFormSet = inlineformset_factory(UserProfile, EmploymentDetails,
                                                form=EmploymentForm, extra=0, can_delete=True)

