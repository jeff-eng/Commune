from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardListView.as_view(), name='dashboard'),
    path('assets/<uuid:pk>', views.AssetDetailView.as_view(), name='asset-detail'),
    path('manage-borrowers', views.manage_borrowers, name='manage-borrowers'),
    path('manage-assets', views.ManageAssetsView.as_view(), name='manage-assets'),
    path('add-asset', views.AddAssetView.as_view(), name='add-asset'),
]