from rest_framework import viewsets
from .models import Product, Category, Brand, Unit
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, UnitSerializer
from common.permissions import IsSuperAdminOrSeller
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get_queryset(self):
        return Category.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]
    def get_queryset(self):
        return Brand.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get_queryset(self):
        return Unit.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get_queryset(self):
        return Product.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
            serializer.save(tenant=self.request.user.tenant)