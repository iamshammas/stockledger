from rest_framework import permissions
from accounts.models import User

class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.role == User.Role.SUPER_ADMIN

class IsSeller(permissions.BasePermission):
    """
    Custom permission to only allow sellers to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.role == User.Role.SELLER

class IsSuperAdminOrSeller(permissions.BasePermission):
    """
    Custom permission to allow superusers and sellers to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.role in [User.Role.SUPER_ADMIN, User.Role.SELLER]

class IsSuperAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow superusers full access and sellers read-only access.
    """

    def has_permission(self, request, view):
        if request.user.role == User.Role.SUPER_ADMIN:
            return True
        elif request.user.role == User.Role.SELLER and request.method in permissions.SAFE_METHODS:
            return True
        return False