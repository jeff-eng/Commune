from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=128, help_text='Enter valid email address (required).')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')