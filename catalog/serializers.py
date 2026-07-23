from rest_framework import serializers
from .models import Product, Category, Brand, Unit

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Product
        fields = '__all__'