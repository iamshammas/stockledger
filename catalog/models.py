from django.db import models
from common.models import TenantScopedModel

class Category(TenantScopedModel):
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ("tenant", "name")


class Brand(TenantScopedModel):
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ("tenant", "name")


class Unit(TenantScopedModel):
    name = models.CharField(max_length=50)        
    short_code = models.CharField(max_length=10, blank=True)

    class Meta:
        unique_together = ("tenant", "name")


class Product(TenantScopedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey(Unit, on_delete=models.RESTRICT)
    sku = models.CharField(max_length=64, blank=True)
    current_selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    low_stock_threshold = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("tenant", "sku")