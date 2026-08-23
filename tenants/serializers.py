from rest_framework import serializers
from .models import Tenant, SellerProfile


class SellerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = SellerProfile
        fields = ["id", "username", "phone_number"]


class TenantListSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    sellers = SellerProfileSerializer(
        source="sellerprofile_set", many=True, read_only=True
    )

    class Meta:
        model = Tenant
        fields = ["id", "name", "owner_username", "sellers", "created_at", "updated_at"]
