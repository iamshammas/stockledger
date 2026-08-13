from .models import Product, Category, Brand, Unit
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, UnitSerializer
from common.permissions import IsSuperAdminOrSeller
from common.views import TenantScopedModelViewSet
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(TenantScopedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]


class BrandViewSet(TenantScopedModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

class UnitViewSet(TenantScopedModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]


class ProductViewSet(TenantScopedModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]
