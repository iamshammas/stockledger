from django.db.models import F, BooleanField, Case, DecimalField, When, Sum, Value, Count
from django.db.models.functions import Coalesce
from decimal import Decimal

from catalog.models import Product
from sales.models import Sale

class ReportService:

    @staticmethod
    def get_current_stock_report(tenant):
        return (
            Product.objects.filter(
            tenant=tenant
            ).select_related("category", "brand", "unit")
            .annotate(
                current_stock=Coalesce(Sum('purchase_items__remaining_quantity'), 
                Value(Decimal("0.000")))
            ).annotate(
                is_low_stock=Case(
                    When(current_stock__lte=F('low_stock_threshold'), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
        )

    @staticmethod
    def get_stock_valuation_report(tenant):
        return (
            Product.objects.filter(
                tenant=tenant
            )
            .annotate(
                current_stock=Coalesce(Sum('purchase_items__remaining_quantity'), 
                Value(Decimal("0.00")))
            ).annotate(
                stock_value=Coalesce(Sum(F('purchase_items__remaining_quantity') * F('purchase_items__buying_price')), 
                Value(Decimal("0.00")), output_field=DecimalField(max_digits=12, decimal_places=2))
            )
        )

    @staticmethod
    def get_daily_sales_report(tenant, date):
        return (
            Sale.objects.filter(
                tenant=tenant,
                invoice_date=date
            ).aggregate(
                total_sales=Coalesce(Sum('total_amount'), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
                total_invoices=Count('id'),
                total_paid=Coalesce(Sum('amount_paid'), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
                total_due=Coalesce(Sum('amount_due'), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2)))
            )
        )