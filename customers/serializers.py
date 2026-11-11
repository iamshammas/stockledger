from rest_framework import serializers

from .models import Retailer


# class RetailerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Retailer
#         fields = "__all__"
#         read_only_fields = ("tenant","id", "credit_balance", "is_active")

class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = ["id", "retailer_name", "shop_name", "phone", "email", "address", "credit_balance", "is_active"]
        read_only_fields = ("tenant","id", "credit_balance", "is_active")