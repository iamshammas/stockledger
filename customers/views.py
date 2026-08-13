from common.views import TenantScopedModelViewSet

from .models import Retailer
from .serializers import RetailerSerializer


class RetailerViewSet(TenantScopedModelViewSet):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer

    def get_queryset(self):
        return (
            Retailer.objects
            .filter(tenant=self.request.user.tenant)
            .order_by("retailer_name")
        )

    