from django.urls import path

from . import views

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('', views.DashboardListView.as_view(), name='dashboard'),
    # path('asset/<uuid:pk>', views.AssetDetailView.as_view(), name='asset-detail'),
    path('asset/<uuid:pk>', views.AssetDetailView.as_view(), name='asset-detail'),
]