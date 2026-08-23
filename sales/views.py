from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse

from payments.models import Payment
from payments.serializers import PaymentCreateSerializer, PaymentSerializer
from sales.models import Sale
from sales.serializers import SaleSerializer
from sales.services import InvoiceService
from common.permissions import IsSuperAdminOrSeller

@extend_schema(tags=["Sales"])
@extend_schema_view(
    list=extend_schema(summary="List All Sales", description="Retrieve a list of all sales."),
    retrieve=extend_schema(summary="Retrieve Sale", description="Retrieve a specific sale by ID."),
    create=extend_schema(summary="Create Sale", description="Create a new sale."),
    update=extend_schema(summary="Update Sale", description="Update an existing sale by ID."),
    partial_update=extend_schema(summary="Partial Update Sale", description="Partially update an existing sale by ID."),
    destroy=extend_schema(summary="Delete Sale", description="Delete a specific sale by ID."),
)
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get_queryset(self):
        return Sale.objects.filter(tenant=self.request.user.tenant).select_related("seller", "retailer").prefetch_related("items")

    def get_serializer_class(self):
        if self.action == 'payments':
            if self.request.method == "POST":
                return PaymentCreateSerializer
            return PaymentSerializer
        return SaleSerializer

    # POST /sales/{pk}/payments/   – record a payment
    # GET  /sales/{pk}/payments/   – list payments for the sale
    @extend_schema(
        request=PaymentCreateSerializer,
        responses={200: PaymentSerializer(many=True), 201: PaymentSerializer},
        summary="Manage Payments for Sale",
        description="Retrieve a list of payments for a specific sale or record a new payment for that sale."
    )
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
        serializer = PaymentCreateSerializer(data=request.data, context={"sale": sale, "user": request.user})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )

    # GET /sales/{pk}/pdf/ – generate a PDF for the sale
    @extend_schema(
        summary="Generate Sale Invoice PDF",
        description="Generate a PDF invoice for a specific sale.",
        responses={200: "PDF file", 404: "Invoice not found."}
    )
    @action(detail=True, methods=["get"], url_path="pdf")
    def pdf(self, request, pk):
        sale = self.get_object()
        pdf_content = InvoiceService.generate_invoice_pdf(sale=sale)

        if pdf_content is None:
            return Response({"detail": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)
        
        response = HttpResponse(pdf_content, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{sale.invoice_number}.pdf"'
        return response
        
