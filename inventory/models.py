from django.db import models
from common.models import TenantScopedModel

class Supplier(TenantScopedModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)


class Purchase(TenantScopedModel):
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    recorded_by = models.ForeignKey("accounts.User", on_delete=models.RESTRICT)
    purchase_date = models.DateField()
    notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.RESTRICT, related_name="purchase_items")
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    remaining_quantity = models.DecimalField(max_digits=12, decimal_places=3)   # FIFO layer tracker
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        PURCHASE = "PURCHASE", "Purchase"
        SALE = "SALE", "Sale"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"
        DAMAGE = "DAMAGE", "Damage"
        RETURN = "RETURN", "Return"

    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE)
    product = models.ForeignKey("catalog.Product", on_delete=models.RESTRICT)
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity_change = models.DecimalField(max_digits=12, decimal_places=3)
    related_purchase_item = models.ForeignKey(PurchaseItem, null=True, blank=True, on_delete=models.SET_NULL)
    related_sale_item = models.ForeignKey(
        "sales.SaleItem", null=True, blank=True, on_delete=models.SET_NULL
    )
    note = models.TextField(blank=True)
    created_by = models.ForeignKey("accounts.User", null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)