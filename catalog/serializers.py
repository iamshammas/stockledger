from django.db.migrations import serializer
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

    def perform_create(self, serializer):
        print('############################')
        print(self.request.user)
        print(self.request.user.tenant)
        print('############################')
        serializer.save(tenant=self.request.user.tenant)

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

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

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

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class ProductSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ["tenant"]