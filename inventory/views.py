from django.shortcuts import render
from inventory.models import Category, Asset, AssetInstance

# View function for "home" page - processed the HTTP request, fetches required data from database, and renders data in HTML page using template, and returns generated HTML in HTTP Response
def index(request):
    """View function for the home page of the site """

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

    return render(request, 'index.html', context=context)