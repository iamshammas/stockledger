from rest_framework.routers import DefaultRouter

from .views import PurchaseViewSet, StockMovementViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r"purchases", PurchaseViewSet, basename="purchase")
router.register(r"stock-movements", StockMovementViewSet, basename="stock-movement")
router.register(r"suppliers", SupplierViewSet, basename="supplier")

urlpatterns = router.urls