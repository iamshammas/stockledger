from django.db import models

from common.models import TenantScopedModel


class Payment(TenantScopedModel):
    sale = models.ForeignKey(
        "sales.Sale", on_delete=models.CASCADE, related_name="payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=30, blank=True)
    note = models.TextField(blank=True)
    recorded_by = models.ForeignKey("accounts.User", on_delete=models.RESTRICT)


class RetailerCredit(TenantScopedModel):
    class Reason(models.TextChoices):
        OVERPAYMENT = "OVERPAYMENT", "Overpayment"
        APPLIED = "APPLIED_TO_INVOICE", "Applied to invoice"
        MANUAL = "MANUAL_ADJUSTMENT", "Manual adjustment"

    retailer = models.ForeignKey("customers.Retailer", on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="credits",
    )
    sale = models.ForeignKey(
        "sales.Sale", null=True, blank=True, on_delete=models.SET_NULL,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=20, choices=Reason.choices)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(
        "accounts.User", null=True, on_delete=models.SET_NULL,
    )
