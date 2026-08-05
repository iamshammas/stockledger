from rest_framework import serializers

from .models import Payment
from .services import PaymentService


class PaymentSerializer(serializers.ModelSerializer):
    """Read-only serializer for listing / retrieving payments."""

    invoice_number = serializers.CharField(
        source="sale.invoice_number", read_only=True,
    )
    # retailer_name = serializers.CharField(
    #     source="sale.retailer.name", read_only=True,
    # )
    # recorded_by_username = serializers.CharField(
    #     source="recorded_by.username", read_only=True,
    # )

    # payments = 
    class Meta:
        model = Payment
        fields = (
            "id",
            "sale",
            "invoice_number",
            # "retailer_name",
            "amount",
            "payment_date",
            "payment_method",
            "note",
            # "recorded_by",
            # "recorded_by_username",
            # "created_at",
        )
        read_only_fields = fields


class PaymentCreateSerializer(serializers.Serializer):
    """Write-only serializer for recording a new payment."""

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_date = serializers.DateField()
    notes = serializers.CharField(required=False, default="", allow_blank=True)

    def create(self, validated_data):
        return PaymentService.record_payment(
            sale=self.context["sale"],
            amount=validated_data["amount"],
            payment_date=validated_data["payment_date"],
            notes=validated_data.get("notes", ""),
            recorded_by=self.context["request"].user,
        )
