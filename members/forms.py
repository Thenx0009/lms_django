from django import forms
from .models import Member
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RoleForm(forms.Form):
    role = forms.ChoiceField(choices=[('Librarian', 'Librarian'), ('Member', 'Member')])


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['user', 'phone_number']
    
    # User registration (you can customize this if needed)
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select User")