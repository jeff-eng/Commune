from django.shortcuts import render
from inventory.models import Category, Asset, AssetInstance

def dashboard(request):
    # Generate counts of some of the main objects
    num_assets = Asset.objects.all().count()
    num_instances = AssetInstance.objects.all().count()

    # Checked out items
    num_instances_checkedout = AssetInstance.objects.filter(checked_out=True).count()

    context = {
        'num_assets': num_assets,
        'num_instances': num_instances,
        'num_instances_checkedout': num_instances_checkedout,
    }

    return render(request, 'dashboard.html', context=context)

def index(request):
    return render(request, 'index.html')