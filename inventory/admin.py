from django.contrib import admin
from .models import Supplier, Purchase, PurchaseItem, StockMovement

admin.site.register([Supplier, Purchase, PurchaseItem, StockMovement])
