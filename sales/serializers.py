from rest_framework import serializers

from sales.models import Sale, SaleItem
from sales.services import SaleService


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        exclude = ("sale",)
        read_only_fields = ("line_total",)

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = "__all__"
        read_only_fields = ("tenant", "seller", "total_amount", "amount_due", "amount_paid", "subtotal", "invoice_number", "status", )

    def create(self, validated_data):
        request = self.context["request"]

        return SaleService().create_sale(
            tenant=request.user.tenant,
            user=request.user,
            validated_data=validated_data,
        )