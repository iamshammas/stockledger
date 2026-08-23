from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Product, Category, Brand, Unit
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, UnitSerializer
from common.permissions import IsSuperAdminOrSeller
from common.views import TenantScopedModelViewSet
from rest_framework.permissions import IsAuthenticated


@extend_schema(tags=["Category"])
@extend_schema_view(
    list=extend_schema(summary="List All Categories", description="Retrieve a list of all product categories."),
    retrieve=extend_schema(summary="Retrieve Category", description="Retrieve a specific product category by ID."),
    create=extend_schema(summary="Create Category", description="Create a new product category."),
    update=extend_schema(summary="Update Category", description="Update an existing product category."),
    partial_update=extend_schema(summary="Partial Update Category", description="Partially update an existing product category."),
    destroy=extend_schema(summary="Delete Category", description="Delete a specific product category by ID."),
)
class CategoryViewSet(TenantScopedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]


@extend_schema(tags=["Brand"])
@extend_schema_view(
    list=extend_schema(summary="List All Brands", description="Retrieve a list of all product brands."),
    retrieve=extend_schema(summary="Retrieve Brand", description="Retrieve a specific product brand by ID."),
    create=extend_schema(summary="Create Brand", description="Create a new product brand."),
    update=extend_schema(summary="Update Brand", description="Update an existing product brand."),
    partial_update=extend_schema(summary="Partial Update Brand", description="Partially update an existing product brand."),
    destroy=extend_schema(summary="Delete Brand", description="Delete a specific product brand by ID."),
)
class BrandViewSet(TenantScopedModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]


@extend_schema(tags=["Unit"])
@extend_schema_view(
    list=extend_schema(summary="List All Units", description="Retrieve a list of all product units."),
    retrieve=extend_schema(summary="Retrieve Unit", description="Retrieve a specific product unit by ID."),
    create=extend_schema(summary="Create Unit", description="Create a new product unit."),
    update=extend_schema(summary="Update Unit", description="Update an existing product unit."),
    partial_update=extend_schema(summary="Partial Update Unit", description="Partially update an existing product unit."),
    destroy=extend_schema(summary="Delete Unit", description="Delete a specific product unit by ID."),
)
class UnitViewSet(TenantScopedModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

@extend_schema(tags=["Product"])
@extend_schema_view(
    list=extend_schema(summary="List All Products", description="Retrieve a list of all products."),
    retrieve=extend_schema(summary="Retrieve Product", description="Retrieve a specific product by ID."),
    create=extend_schema(summary="Create Product", description="Create a new product."),
    update=extend_schema(summary="Update Product", description="Update an existing product."),
    partial_update=extend_schema(summary="Partial Update Product", description="Partially update an existing product."),
    destroy=extend_schema(summary="Delete Product", description="Delete a specific product by ID."),
)
class ProductViewSet(TenantScopedModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]
