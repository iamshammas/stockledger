from django.urls import path
from .views import CurrentStockAPIView, StockValuationAPIView

urlpatterns = [
    path('current-stock/', CurrentStockAPIView.as_view(), name='current-stock'),
    path('stock-valuation/', StockValuationAPIView.as_view(), name='stock-valuation')
]

