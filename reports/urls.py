from django.urls import path
from .views import CurrentStockAPIView, DailySalesAPIView, MonthlySalesAPIView, PurchaseHistoryAPIView, RetailerDuesAPIView, StockValuationAPIView

urlpatterns = [
    path('current-stock/', CurrentStockAPIView.as_view(), name='current-stock'),
    path('stock-valuation/', StockValuationAPIView.as_view(), name='stock-valuation'),
    path('daily-sales/', DailySalesAPIView.as_view(), name='daily-sales'),
    path('monthly-sales/', MonthlySalesAPIView.as_view(), name='monthly-sales'),
    path('retailer-dues/', RetailerDuesAPIView.as_view(), name='retailer-dues'),
    path('purchase-history/', PurchaseHistoryAPIView.as_view(), name='purchase-history'),
]

