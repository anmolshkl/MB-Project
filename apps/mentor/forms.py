from django import forms
from apps.user.models import UserProfile
from apps.mentor.models import EducationDetails, EmploymentDetails
from django.forms import DateField
from django.forms.models import inlineformset_factory


class EmploymentForm(forms.ModelForm):
    class Meta:
        model = EmploymentDetails
        fields = ('organization', 'location', 'position', 'from_year', 'to_year')
        widgets = {
            'from_year': forms.TextInput(attrs={'placeholder': '2012'}),
            'to_year': forms.TextInput(attrs={'placeholder': '2013'}),
            'location': forms.TextInput(attrs={'placeholder': 'Menlo Park, CA-USA'}),
            'organization': forms.TextInput(attrs={'placeholder': 'SAP'}),
            'position': forms.TextInput(attrs={'placeholder': 'Business Analyst'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationDetails
        fields = ('institution', 'city', 'state', 'country', 'degree', 'branch', 'from_year', 'to_year')
        widgets = {
            'from_year': forms.TextInput(attrs={'placeholder': '2010'}),
            'to_year': forms.TextInput(attrs={'placeholder': '2014'}),
            'city': forms.TextInput(attrs={'placeholder': 'Pittsburgh'}),
            'state': forms.TextInput(attrs={'placeholder': 'Pennsylvania, if any'}),
            'country': forms.TextInput(attrs={'placeholder': 'USA'}),
            'degree': forms.TextInput(attrs={'placeholder': 'MS'}),
            'branch': forms.TextInput(attrs={'placeholder': 'MIS'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender', 'date_of_birth', 'contact', 'city', 'country', 'about', 'picture', 'resume')
        widgets = {
            'about': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Please enter a description here'}),
            'contact': forms.TextInput(attrs={'placeholder': 'eg +91 9970631445'}),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'MM/DD/YYYY'}, format="%m/%d/%Y"),
            'city': forms.TextInput(attrs={'placeholder': 'Barcelona'}),
            'country': forms.TextInput(attrs={'placeholder': 'Spain'}),
        }


EducationDetailsFormSet = inlineformset_factory(UserProfile, EducationDetails,
                                                form=EducationForm, extra=0, can_delete=True)
EmploymentDetailsFormSet = inlineformset_factory(UserProfile, EmploymentDetails,
                                                 form=EmploymentForm, extra=0, can_delete=True)

