from django.db.models import F, BooleanField, Case, DecimalField, When, Sum, Value, Count
from django.db.models.functions import Coalesce, TruncMonth
from decimal import Decimal

from catalog.models import Product
from inventory.models import PurchaseItem
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

    @staticmethod
    def get_monthly_sales_report(tenant, year):
        return (
            Sale.objects.filter(
                tenant=tenant,
                invoice_date__year=year
            ).values(month=TruncMonth('invoice_date'))
            .annotate(
                total_sales=Coalesce(Sum('total_amount'), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
                total_invoices=Count('id'),
                total_paid=Coalesce(Sum('amount_paid'), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
                total_due=Coalesce(Sum('amount_due'), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2)))
            ).order_by('month')
        )

    @staticmethod
    def get_retailer_dues_report(tenant):
        return (
            Sale.objects.filter(
                tenant=tenant,
                amount_due__gt=0
            ).values(
                retailer_pk = F('retailer__id'), 
                retailer_name = F('retailer__retailer_name'))
            .annotate(
                total_due=Coalesce(Sum('amount_due'), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2))),
                total_invoices=Count('id')
            ).order_by('-total_due')
        )

    @staticmethod
    def get_product_purchase_report(tenant):
        return (
            PurchaseItem.objects.filter(
                purchase__tenant=tenant
            ).select_related('product', 'purchase')
            .values(
                'product_id',
                product_name=F('product__name')
            ).annotate(
                total_quantity_purchased=Coalesce(Sum('quantity'), Value(Decimal("0.000"), output_field=DecimalField(max_digits=12, decimal_places=3))),
                total_purchase_value=Coalesce(Sum(F('quantity') * F('buying_price')), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2)))
            )
        )

    @staticmethod
    def get_daily_purchase_report(tenant, start_date, end_date):
        return (
            PurchaseItem.objects.filter(
                purchase__tenant=tenant,
                purchase__purchase_date__range=[start_date, end_date]
            ).select_related('product', 'purchase')
            .values(
                date=F('purchase__purchase_date'),
                product_name=F('product__name'))
            .annotate(
                total_quantity_purchased=Coalesce(Sum('quantity'), Value(Decimal("0.000"), output_field=DecimalField(max_digits=12, decimal_places=3))),
                total_purchase_value=Coalesce(Sum(F('quantity') * F('buying_price')), Value(Decimal("0.00"), output_field=DecimalField(max_digits=12, decimal_places=2)))
            ).order_by('date')
        )

    @staticmethod
    def get_low_stock_report(tenant):
        return (
            Product.objects.filter(
                tenant=tenant)
            .annotate(
                current_stock=Coalesce(Sum('purchase_items__remaining_quantity'), 
                Value(Decimal("0.000")))
            ).filter(
                current_stock__lte=F('low_stock_threshold')
            )
        ) 

