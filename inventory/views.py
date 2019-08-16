from django.shortcuts import render
from django.views.generic.base import TemplateView
from inventory.models import Category, Borrower, Asset

def index(request):
    return render(request, 'index.html')

def manage_borrowers(request):
    return render(request, 'inventory/manage_borrowers.html')

class ManageAssetsView(TemplateView):
    template_name = 'inventory/manage_assets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Asset.objects.all()
        context['categories'] = Category.objects.all()
        return context

class AddAssetView(TemplateView):
    template_name = 'inventory/add_asset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardListView(LoginRequiredMixin, generic.ListView):
    model = Asset
    template_name = 'inventory/asset_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Asset.objects.filter(owner=self.request.user)

    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

class AssetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Asset