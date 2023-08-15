from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField()
  address = forms.CharField()
  type = forms.ChoiceField(choices=Profile.USER_CHOICES)

  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'address', 'type']
