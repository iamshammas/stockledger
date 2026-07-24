from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Purchase, StockMovement
from .serializers import PurchaseSerializer, StockMovementSerializer


class PurchaseViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.filter(
            tenant=self.request.user.tenant
        ).select_related("supplier", "recorded_by")

class StockMovementViewSet(ReadOnlyModelViewSet):
    serializer_class = StockMovementSerializer

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