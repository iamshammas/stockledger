from common.models import TenantScopedModel
from django.db import models

class Retailer(TenantScopedModel):
    retailer_name = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    credit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "phone"], name="unique_retailer_phone_per_tenant")
        ]
        unique_together = ("tenant", "phone")