from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsSuperAdmin

from .serializers import CurrentUserSerializer, SellerRegistrationSerializer
from .services import AccountService

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SellerRegistrationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        serializer = SellerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AccountService.register_seller(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
            tenant_name=serializer.validated_data["tenant_name"],
            phone_number=serializer.validated_data["phone_number"],
        )

        return Response(
            CurrentUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )