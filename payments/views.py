from datetime import date

from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(ReadOnlyModelViewSet):
    """
    Global payment listing and detail.

    GET /payments/
    GET /payments/{id}/

    Supports optional date filtering via query parameters:
        ?from=YYYY-MM-DD
        ?to=YYYY-MM-DD
    """

    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = (
            Payment.objects
            .filter(tenant=self.request.user.tenant)
            .select_related("sale__retailer", "recorded_by")
            .order_by("-payment_date", "-created_at")
        )

        date_from = self.request.query_params.get("from")
        date_to = self.request.query_params.get("to")

        if date_from:
            queryset = queryset.filter(payment_date__gte=date_from)

        if date_to:
            queryset = queryset.filter(payment_date__lte=date_to)

        if date_from and date_to and date_from > date_to:
            raise ValidationError(
                {"date_range": "'from' date must not be after 'to' date."}
            )

        return queryset
