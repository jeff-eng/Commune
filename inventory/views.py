from django.shortcuts import render
from inventory.models import Category, Asset, AssetInstance

def index(request):
    return render(request, 'index.html')


from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardListView(LoginRequiredMixin, generic.ListView):
    model = Asset

    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'