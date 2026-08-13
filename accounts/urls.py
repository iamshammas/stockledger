from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from .views import SellerRegistrationAPIView, CurrentUserView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", CurrentUserView.as_view(), name="current_user"),

    path("accounts/sellers/", SellerRegistrationAPIView.as_view(), name="seller_create"),
]
