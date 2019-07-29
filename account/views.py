from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from account.forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django.views import View

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
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'registration_form': form})