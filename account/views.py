from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from account.forms import ChangePasswordForm, UserRegistrationForm
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy

class UserRegistrationView(View):
    form_class = UserRegistrationForm
    initial = {'key': 'value'}
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'registration_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Process form cleaned data
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return HttpResponseRedirect('/dashboard')

        return render(request, self.template_name, {'registration_form': form})

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'account/password_success.html', {})