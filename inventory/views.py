from django.views import generic
from django.http import JsonResponse
from django import forms
from django.shortcuts import render
from inventory.models import Category, Borrower, Asset
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, 'index.html')

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['checked_out', 'return_date', 'borrower']

class DashboardListView(LoginRequiredMixin, generic.ListView):
    model = Asset
    template_name = 'inventory/asset_list.html'
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Asset.objects.filter(owner=self.request.user)

class AssetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Asset

class AssetReturn(generic.View):
    def post(self, request, pk):
        data = dict()
        asset = Asset.objects.get(pk=pk)
        if asset:
            asset.checked_out = False
            asset.return_date = None
            asset.borrower = None
            print("Server was pinged.")
            asset.save()
            data['message'] = "Asset returned!"
        else:
            data['message'] = "Error!"
        return JsonResponse(data)