from rest_framework import viewsets


class TenantScopedModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.queryset.filter(
            tenant=self.request.user.tenant
        )

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant
        )