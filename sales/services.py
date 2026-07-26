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

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

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

        # Process line items with FIFO allocation
        subtotal = SaleService._process_items(
            sale=sale,
            items_data=items_data,
            tenant=tenant,
            user=user,
        )

        # Calculate totals and persist
        SaleService._recalculate_totals(sale, subtotal)

        return sale

    @staticmethod
    @transaction.atomic
    def update_sale(*, sale, validated_data, user):
        """
        Single entry point for editing an existing invoice.

        Accepts the existing sale instance, validated (edited) data,
        and the seller/user performing the update.
        """
        tenant = sale.tenant

        # --- 1. Extract items from the payload -----------------------
        items_data = validated_data.pop("items")

        # --- 2. Update editable Sale-level fields --------------------
        editable_fields = ["retailer", "invoice_date", "notes"]
        updated_fields = []

        for field in editable_fields:
            if field in validated_data:
                setattr(sale, field, validated_data[field])
                updated_fields.append(field)

        # Mark the invoice as edited
        sale.is_edited = True
        updated_fields.append("is_edited")

        # --- 3. Reverse all inventory effects of the old sale --------
        SaleService._reverse_sale(sale)

        # --- 4. Apply the edited invoice using FIFO logic ------------
        subtotal = SaleService._process_items(
            sale=sale,
            items_data=items_data,
            tenant=tenant,
            user=user,
        )

        # --- 5. Recalculate totals and payment status ----------------
        SaleService._recalculate_totals(sale, subtotal, extra_fields=updated_fields)

        return sale

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _process_items(*, sale, items_data, tenant, user):
        """
        Create SaleItems from *items_data*, deduct stock using FIFO,
        and record SaleItemCostAllocations + StockMovements.

        Returns the calculated subtotal across all line items.

        Must be called inside an existing @transaction.atomic block.
        """
        subtotal = Decimal("0.00")

        for item_data in items_data:
            purchase_batches = (
                PurchaseItem.objects
                .select_for_update()
                .filter(product=item_data["product"], remaining_quantity__gt=0)
                .order_by("purchase__purchase_date", "id",)
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

        return subtotal

    @staticmethod
    def _recalculate_totals(sale, subtotal, *, extra_fields=None):
        """
        Set subtotal, total_amount, amount_due, and payment status
        on the given sale, then persist the changes.

        *extra_fields* is an optional list of additional field names
        that have been changed on the sale object and should be
        included in the save() call.

        Must be called inside an existing @transaction.atomic block.
        """
        sale.subtotal = subtotal
        sale.total_amount = subtotal  # No additional charges for now

        # Honour any payments already recorded against this invoice
        sale.amount_due = sale.total_amount - sale.amount_paid

        # Derive payment status
        if sale.amount_due <= Decimal("0.00"):
            sale.status = Sale.Status.PAID
        elif sale.amount_paid > Decimal("0.00"):
            sale.status = Sale.Status.PARTIAL
        else:
            sale.status = Sale.Status.UNPAID

        fields_to_save = [
            "subtotal", "total_amount", "amount_due", "status",
        ]
        if extra_fields:
            fields_to_save.extend(extra_fields)

        sale.save(update_fields=fields_to_save)

    @staticmethod
    def _reverse_sale(sale):
        """
        Reverse all inventory effects of an existing sale.

        This helper undoes FIFO allocations, restores purchase-batch
        stock, and removes related SaleItems / StockMovements.

        It does NOT delete the Sale object itself, nor does it
        modify invoice totals, payment fields, or the invoice number.

        Must be called inside an existing @transaction.atomic block.
        """

        sale_items = sale.items.select_related("product")

        for sale_item in sale_items:

            # --- 1. Restore stock from each FIFO allocation -----------
            allocations = sale_item.cost_allocations.select_related(
                "purchase_item",
            )

            for allocation in allocations:
                purchase_item = allocation.purchase_item

                # Give back the quantity that was consumed from this batch
                purchase_item.remaining_quantity += allocation.quantity
                purchase_item.save(update_fields=["remaining_quantity"])

            # --- 2. Delete the FIFO cost-allocation records -----------
            allocations.delete()

            # --- 3. Delete SALE stock-movement records ----------------
            StockMovement.objects.filter(
                movement_type=StockMovement.MovementType.SALE,
                related_sale_item=sale_item,
            ).delete()

        # --- 4. Delete all SaleItems (the Sale itself is kept) --------
        sale_items.delete()