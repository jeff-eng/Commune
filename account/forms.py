from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from account.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=128, help_text='Enter valid email address (required).')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

class ChangePasswordForm(PasswordChangeForm):
    __input_classes = 'uk-input uk-width-1-1@s uk-form-width-medium uk-margin-bottom'
    
    old_password = forms.CharField(max_length = 100, widget=forms.PasswordInput(attrs={'class': __input_classes, 'placeholder': 'Enter Old Password'}))
    new_password1 = forms.CharField(max_length = 100, widget=forms.PasswordInput(attrs={'class': __input_classes, 'placeholder': 'Enter New Password'}))
    new_password2 = forms.CharField(max_length = 100, widget=forms.PasswordInput(attrs={'class': __input_classes, 'placeholder': 'Confirm New Password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')