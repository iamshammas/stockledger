from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsSuperAdminOrReadOnly, IsSuperAdminOrSeller
from common.views import TenantScopedModelViewSet
from .models import Purchase, StockMovement, Supplier
from .serializers import PurchaseSerializer, StockMovementSerializer, SupplierSerializer


class SupplierViewSet(TenantScopedModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

class PurchaseViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get_queryset(self):
        return Purchase.objects.filter(
            tenant=self.request.user.tenant
        ).select_related("supplier", "recorded_by")

class StockMovementViewSet(ReadOnlyModelViewSet):
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

    def get_queryset(self):
        queryset = (
            StockMovement.objects
            .filter(tenant=self.request.user.tenant)
            .select_related("product")
            .order_by("-created_at")
        )

        product = self.request.query_params.get("product")
        if product:
            queryset = queryset.filter(product_id=product)

        return queryset