from rest_framework import serializers
from catalog.models import Product

class CurrentStockSerializer(serializers.ModelSerializer):
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

