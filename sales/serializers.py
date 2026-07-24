from rest_framework import serializers

from sales.models import Sale, SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        exclude = ("sale",)

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = "__all__"
        read_only_fields = ("tenant", "seller", "total_amount", "amount_due", "amount_paid", "subtotal", "invoice_number", "status", )

    def create(self, validated_data):
        request = self.context["request"]

        return Sale.objects.create_sale(
            tenant=request.user.tenant,
            seller=request.user,
            validated_data=validated_data,
        )