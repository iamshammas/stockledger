from rest_framework import serializers
from catalog.models import Product

class CurrentStockReportSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id')
    product_name = serializers.CharField(source='name')
    category = serializers.CharField(source='category.name')
    brand = serializers.CharField(source='brand.name')
    unit = serializers.CharField(source='unit.name')
    current_stock = serializers.DecimalField(max_digits=12, decimal_places=3, read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    class Meta:
        model = Product
        fields = ["product_id", "product_name", "category", "brand", "unit", "current_stock", "low_stock_threshold", "is_low_stock"]

class StockValuationReportSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='id')
    product_name = serializers.CharField(source='name')

    current_stock = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    stock_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ["product_id", "product_name", "current_stock", "stock_value"]

class DailySalesReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_invoices = serializers.IntegerField()
    total_paid = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_due = serializers.DecimalField(max_digits=12, decimal_places=2)

class MonthlySalesReportSerializer(serializers.Serializer):
    month = serializers.DateField(format="%Y-%m")
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_invoices = serializers.IntegerField()
    total_paid = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_due = serializers.DecimalField(max_digits=12, decimal_places=2)

class RetailerDuesReportSerializer(serializers.Serializer):
    retailer_id = serializers.IntegerField(source='retailer_pk')
    retailer_name = serializers.CharField()
    total_due = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_invoices = serializers.IntegerField()

class DailyPurchaseReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    product_name = serializers.CharField()
    total_quantity_purchased = serializers.DecimalField(max_digits=12, decimal_places=3)
    total_purchase_value = serializers.DecimalField(max_digits=12, decimal_places=2)


class ProductPurchaseReportSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_quantity_purchased = serializers.DecimalField(max_digits=12, decimal_places=3)
    total_purchase_value = serializers.DecimalField(max_digits=12, decimal_places=2)
