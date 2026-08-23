from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsSuperAdmin

from accounts.views import SellerRegistrationAPIView
from .models import Tenant
from .serializers import TenantListSerializer


class TenantListCreate(APIView):
    """
    GET  — List all tenants with their seller profiles (SuperAdmin only).
    POST — Delegates to SellerRegistrationAPIView to avoid duplicating
           the registration logic.
    """

    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        tenants = Tenant.objects.select_related("owner").prefetch_related(
            "sellerprofile_set__user"
        ).all()
        serializer = TenantListSerializer(tenants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        return SellerRegistrationAPIView().post(request)
