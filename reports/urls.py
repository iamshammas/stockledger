from django.urls import path
from .views import CurrentStockAPIView

urlpatterns = [
    path('current-stock/', CurrentStockAPIView.as_view(), name='current-stock'),
]

# dashboard

