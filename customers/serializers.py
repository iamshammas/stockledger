from rest_framework import serializers

from .models import Retailer


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = "__all__"
        read_only_fields = ("tenant",)