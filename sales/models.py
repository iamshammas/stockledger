from django.db import models
from common.models import TenantScopedModel

class InvoiceSequence(models.Model):
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE)
    period_key = models.CharField(max_length=20)     
    last_number = models.IntegerField(default=0)

    class Meta:
        unique_together = ("tenant", "period_key")


class Sale(TenantScopedModel):
    class Status(models.TextChoices):
        PAID = "PAID", "Paid"
        PARTIAL = "PARTIAL", "Partial"
        UNPAID = "UNPAID", "Unpaid"

    retailer = models.ForeignKey("customers.Retailer", on_delete=models.RESTRICT)
    seller = models.ForeignKey("accounts.User", on_delete=models.RESTRICT)
    invoice_number = models.CharField(max_length=30)
    invoice_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UNPAID)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_due = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        unique_together = ("tenant", "invoice_number")


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SaleItemCostAllocation(models.Model):
    sale_item = models.ForeignKey(SaleItem, on_delete=models.CASCADE, related_name="cost_allocations")
    purchase_item = models.ForeignKey("inventory.PurchaseItem", on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)