from django.contrib import admin
from sales.models import InvoiceSequence, Sale, SaleItem, SaleItemCostAllocation

admin.site.register(InvoiceSequence)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(SaleItemCostAllocation)