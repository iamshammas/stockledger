from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsSuperAdminOrReadOnly, IsSuperAdminOrSeller
from .models import Purchase, StockMovement, Supplier
from .serializers import PurchaseSerializer, StockMovementSerializer, SupplierSerializer


class SupplierViewSet(ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get_queryset(self):
        return Supplier.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

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