from rest_framework.viewsets import ModelViewSet

from .models import Retailer
from .serializers import RetailerSerializer


class RetailerViewSet(ModelViewSet):
    serializer_class = RetailerSerializer

    def get_queryset(self):
        return (
            Retailer.objects
            .filter(tenant=self.request.user.tenant)
            .order_by("retailer_name")
        )

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

    