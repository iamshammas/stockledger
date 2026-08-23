from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsSuperAdminOrReadOnly, IsSuperAdminOrSeller
from common.views import TenantScopedModelViewSet
from .models import Purchase, StockMovement, Supplier
from .serializers import PurchaseSerializer, StockMovementSerializer, SupplierSerializer

@extend_schema(tags=["Suppliers"])
@extend_schema_view(
    list=extend_schema(summary="List All Suppliers", description="Retrieve a list of all suppliers."),
    retrieve=extend_schema(summary="Retrieve Supplier", description="Retrieve a specific supplier by ID."),
    create=extend_schema(summary="Create Supplier", description="Create a new supplier."),
    update=extend_schema(summary="Update Supplier", description="Update an existing supplier."),
    partial_update=extend_schema(summary="Partial Update Supplier", description="Partially update an existing supplier."),
    destroy=extend_schema(summary="Delete Supplier", description="Delete a specific supplier by ID."),
)
class SupplierViewSet(TenantScopedModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

@extend_schema(tags=["Purchases"])
@extend_schema_view(
    list=extend_schema(summary="List All Purchases", description="Retrieve a list of all purchases."),
    retrieve=extend_schema(summary="Retrieve Purchase", description="Retrieve a specific purchase by ID."),
    create=extend_schema(summary="Create Purchase", description="Create a new purchase."),
    update=extend_schema(summary="Update Purchase", description="Update an existing purchase."),
    partial_update=extend_schema(summary="Partial Update Purchase", description="Partially update an existing purchase."),
    destroy=extend_schema(summary="Delete Purchase", description="Delete a specific purchase by ID."),
)
class PurchaseViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get_queryset(self):
        return Purchase.objects.filter(
            tenant=self.request.user.tenant
        ).select_related("supplier", "recorded_by")

@extend_schema(tags=["Stock Movements"], summary="Retrieve Stock Movements", description="Retrieve a list of stock movements for products.")
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