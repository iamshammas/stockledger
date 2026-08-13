from rest_framework import serializers
from .models import User
from tenants.models import SellerProfile

class CurrentUserSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "role", "tenant", "tenant_name"]

class SellerRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)
    tenant_name = serializers.CharField(max_length=255, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    def validate_tenant_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Tenant name cannot be blank.")
        return value

    def validate_phone_number(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Phone number cannot be blank.")
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits long.")
        if SellerProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A seller with this phone number is already registered.")
        return value