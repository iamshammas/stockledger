from rest_framework import viewsets
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status

class TenantScopedModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.SUPER_ADMIN:
            tenant = self.request.query_params.get('tenant')
            if not tenant:
                return Response({'status': 'Tenant id is not there'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return self.queryset.filter(tenant__id=tenant)
        return self.queryset.filter(tenant=user.tenant)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.SUPER_ADMIN:
            tenant = self.request.data.get('tenant')
            if not tenant:
                return Response({'status': 'Tenant id is not there'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer.save(tenant_id=tenant)
        else:
            serializer.save(tenant=user.tenant)