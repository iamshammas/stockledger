from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from sales.models import Sale
from sales.serializers import SaleSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Sale.objects.filter(tenant=self.request.user.tenant).select_related("seller", "customer").prefetch_related("sale_items")
