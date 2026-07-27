from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentCreateSerializer, PaymentSerializer
from sales.models import Sale
from sales.serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Sale.objects.filter(tenant=self.request.user.tenant).select_related("seller", "retailer").prefetch_related("items")

    # POST /sales/{pk}/payments/   – record a payment
    # GET  /sales/{pk}/payments/   – list payments for the sale
    @action(detail=True, methods=["get", "post"], url_path="payments")
    def payments(self, request, pk=None):
        sale = self.get_object()

        if request.method == "GET":
            payments = (
                Payment.objects
                .filter(sale=sale, tenant=request.user.tenant)
                .select_related("sale__retailer", "recorded_by")
                .order_by("-created_at")
            )
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)

        # POST
        serializer = PaymentCreateSerializer(
            data=request.data,
            context={"request": request, "sale": sale},
        )
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )
