from django.urls import path
from . import views
import inventory.views

urlpatterns = [
    path('', views.index),
    path('dashboard/', views.DashboardListView.as_view(), name='dashboard'),
    path('assets/<uuid:pk>', views.AssetDetailView.as_view(), name='asset-detail'),
    path('assets/return/<uuid:pk>', views.AssetReturn.as_view(), name='asset_return'),
]