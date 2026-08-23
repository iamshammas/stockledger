from drf_spectacular.utils import extend_schema, extend_schema_view

from common.views import TenantScopedModelViewSet
from .models import Retailer
from .serializers import RetailerSerializer

@extend_schema(tags=["Retailers"])
@extend_schema_view(
    list=extend_schema(summary="List All Retailers", description="Retrieve a list of all retailers."),
    retrieve=extend_schema(summary="Retrieve Retailer", description="Retrieve a specific retailer by ID."),
    create=extend_schema(summary="Create Retailer", description="Create a new retailer."),
    update=extend_schema(summary="Update Retailer", description="Update an existing retailer."),
    partial_update=extend_schema(summary="Partial Update Retailer", description="Partially update an existing retailer."),
    destroy=extend_schema(summary="Delete Retailer", description="Delete a specific retailer by ID."),
)
class RetailerViewSet(TenantScopedModelViewSet):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer

    def get_queryset(self):
        return (
            Retailer.objects
            .filter(tenant=self.request.user.tenant)
            .order_by("retailer_name")
        )

    