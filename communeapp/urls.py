"""communeapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from inventory.api import api_views
import inventory.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Directs to the urls.py file within the inventory app
    path('', include('inventory.urls')),
]

urlpatterns += [
    # Django site authentication URLs for login/logout/password management
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('api/v1/asset/', api_views.AssetList.as_view()),
    path('api/v1/asset/create', api_views.AssetCreate.as_view(), name='asset_create'),
    path('api/v1/borrower/create', api_views.BorrowerCreate.as_view(), name='borrower_create'),
    path('api/v1/category/create', api_views.CategoryCreate.as_view(), name='category_create'),
    path('api/v1/asset/<uuid:uid>/', api_views.AssetRetrieveUpdateDestroy.as_view()),
    path('api/v1/category/', api_views.CategoryList.as_view()),
]