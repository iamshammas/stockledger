from rest_framework.routers import DefaultRouter
from .views import RetailerViewSet

router = DefaultRouter()
router.register(r"retailers", RetailerViewSet, basename="retailer")

urlpatterns = router.urls