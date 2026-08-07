from django.urls import path
from .views import CurrentStockAPIView, DailySalesAPIView, StockValuationAPIView

urlpatterns = [
    path('current-stock/', CurrentStockAPIView.as_view(), name='current-stock'),
    path('stock-valuation/', StockValuationAPIView.as_view(), name='stock-valuation'),
    path('daily-sales/', DailySalesAPIView.as_view(), name='daily-sales'),
]

# daily-sales/?date=YYYY-MM-DD