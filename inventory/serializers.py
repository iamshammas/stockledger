from rest_framework import serializers

from .models import Purchase, PurchaseItem, StockMovement
from .services import PurchaseService


class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = (
            "product",
            "quantity",
            "buying_price",
            "selling_price",
        )


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)

    class Meta:
        model = Purchase
        fields = (
            "id",
            "supplier",
            "purchase_date",
            "notes",
            "total_amount",
            "items",
        )
        read_only_fields = ("id", "total_amount")

    def create(self, validated_data):
        request = self.context["request"]

        return PurchaseService.create_purchase(
            tenant=request.user.tenant,
            user=request.user,
            validated_data=validated_data,
        )

class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = StockMovement
        fields = (
            "id",
            "product",
            "product_name",
            "movement_type",
            "quantity_change",
            "created_at",
        )