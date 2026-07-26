from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from jsonschema import ValidationError

from inventory.models import PurchaseItem, StockMovement

from .models import InvoiceSequence, Sale, SaleItem, SaleItemCostAllocation

class InvoiceService:

    @staticmethod
    @transaction.atomic
    def generate_number(tenant):
        period_key = timezone.now().strftime("%Y%m%d")

        sequence, _ = InvoiceSequence.objects.select_for_update().get_or_create(
            tenant=tenant,
            period_key=period_key,
            defaults={"last_number": 0},
        )

        sequence.last_number += 1
        sequence.save(update_fields=["last_number"])

        return f"INV-{period_key}-{sequence.last_number:06d}"

class SaleService:

    @staticmethod
    @transaction.atomic
    def create_sale(*, tenant, user, validated_data):
        items_data = validated_data.pop("items")

        invoice_number = InvoiceService.generate_number(tenant)

        sale = Sale.objects.create(
            tenant=tenant,
            seller=user,
            invoice_number=invoice_number,
            **validated_data,
        )

        subtotal = Decimal("0.00")

        for item_data in items_data:
            purchase_batches = (
                PurchaseItem.objects
                .select_for_update()
                .filter(product=item_data["product"], remaining_quantity__gt=0)
                .order_by("purchase__purchase_date","id",)
            )

            available_quantity = sum(batch.remaining_quantity for batch in purchase_batches)
            if available_quantity < item_data["quantity"]:
                raise ValidationError(f"Not enough stock for product {item_data['product'].name}")

            sale_item = SaleItem.objects.create(
                            sale=sale,
                            product=item_data["product"],
                            quantity=item_data["quantity"],
                            selling_price=item_data["selling_price"],
                            line_total=item_data["quantity"] * item_data["selling_price"],
                        )

            subtotal += sale_item.line_total
            quantity_to_sell = item_data["quantity"]

            for batch in purchase_batches:
                if quantity_to_sell == 0:
                    break

                # Determine how much to consume from this batch        
                consumed = min(quantity_to_sell, batch.remaining_quantity)

                # Update the remaining quantity of the batch
                batch.remaining_quantity -= consumed
                batch.save(update_fields=["remaining_quantity"])

                quantity_to_sell -= consumed

                # Create a SaleItemCostAllocation record to track which purchase batch was used for this sale item
                SaleItemCostAllocation.objects.create(
                    sale_item=sale_item,
                    purchase_item=batch,
                    quantity=consumed,
                    unit_cost=batch.buying_price,
                )

                # Create a StockMovement record for the sale    
                StockMovement.objects.create(
                    tenant=tenant,
                    product=batch.product,
                    movement_type=StockMovement.MovementType.SALE,
                    quantity_change=-consumed,
                    related_purchase_item=batch,
                    related_sale_item=sale_item,
                    created_by=user,
                )

        sale.subtotal = subtotal
        sale.total_amount = subtotal  # Assuming no additional charges for simplicity
        sale.amount_due = subtotal  # Assuming no payments made yet
        
        sale.save(update_fields=["subtotal", "total_amount", "amount_due"])

        return sale