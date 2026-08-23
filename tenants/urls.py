from django.urls import path
from . import views


urlpatterns = [
    path('', views.TenantListCreate.as_view(), name='tenant-list-create'),
]