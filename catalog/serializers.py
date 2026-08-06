from rest_framework import serializers
from .models import Product, Category, Brand, Unit

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ["tenant"]

    def validate_name(self, value):
        tenant = self.context['request'].user.tenant
        queryset = Category.objects.filter(name__iexact=value, tenant=tenant)

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Category with this name already exists for this tenant.")
        return value


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        read_only_fields = ["tenant"]

    def validate_name(self, value):
        tenant = self.context['request'].user.tenant
        queryset = Brand.objects.filter(name__iexact=value, tenant=tenant)

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Brand with this name already exists for this tenant.")
        return value

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ["tenant"]

    def validate_name(self, value):
        tenant = self.context['request'].user.tenant
        queryset = Unit.objects.filter(name__iexact=value, tenant=tenant)

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Unit with this name already exists for this tenant.")
        return value


class ProductSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "brand",
            "unit",
            "sku",
            "current_selling_price",
            "low_stock_threshold"
        )
        read_only_fields = ["tenant", "created_at", "updated_at", "id"]