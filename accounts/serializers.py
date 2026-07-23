from rest_framework import serializers
from .models import User

class CurrentUserSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "role", "tenant", "tenant_name"]