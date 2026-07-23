from django.db import models
from common.models import TimeStampedModel

class Tenant(TimeStampedModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        "accounts.User", on_delete=models.RESTRICT, related_name="owned_tenants"
    )


class SellerProfile(TimeStampedModel):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)