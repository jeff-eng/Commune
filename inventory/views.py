from django.shortcuts import render
from inventory.models import Category, Borrower, Asset

def index(request):
    return render(request, 'index.html')


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