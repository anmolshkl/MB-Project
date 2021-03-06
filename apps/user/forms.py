from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    """ Require email address when a user signs up """
    email = forms.EmailField(label='Email address', max_length=75)
    
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name')
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': ''}),
            'first_name': forms.TextInput(attrs={'placeholder': ''}),
        }     

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
        except User.DoesNotExist:
            return email
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = user.email
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
            
        return user


class UserEditForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets={
            'email': forms.TextInput(attrs={'readonly': 'True'}),
        }

    def clean_email(self):
        if self.instance:
            return self.instance.email
        else:
            return self.fields['email']

