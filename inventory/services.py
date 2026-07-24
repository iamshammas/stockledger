from django.db import transaction
from inventory.models import Purchase, PurchaseItem, StockMovement


class PurchaseService:

    @staticmethod
    @transaction.atomic
    def create_purchase(*, tenant, user, validated_data):
        items_data = validated_data.pop("items")
        purchase = Purchase.objects.create(
            tenant=tenant,
            recorded_by=user,
            **validated_data
        )

        total_amount = 0
        for item_data in items_data:
            purchase_item = PurchaseItem.objects.create(
                purchase=purchase,
                product=item_data["product"],
                quantity=item_data["quantity"],
                remaining_quantity=item_data["quantity"],
                buying_price=item_data["buying_price"],
                selling_price=item_data["selling_price"],
            )
            StockMovement.objects.create(
                tenant=tenant,
                product=purchase_item.product,
                movement_type=StockMovement.MovementType.PURCHASE,
                quantity_change=purchase_item.quantity,
                related_purchase_item=purchase_item,
                created_by=user,
            )
            total_amount += purchase_item.quantity * purchase_item.buying_price

        purchase.total_amount = total_amount
        purchase.save(update_fields=["total_amount"])

        return purchase