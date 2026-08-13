from django.db import transaction

from accounts.models import User
from tenants.models import Tenant, SellerProfile


class AccountService:

    @staticmethod
    def _create_user_account(*, username, password):
        """Create a User account. Role and tenant are assigned by the caller."""
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        return user

    @staticmethod
    def _create_tenant(*, name, owner):
        """Create a Tenant owned by the given user."""
        tenant = Tenant.objects.create(
            name=name,
            owner=owner,
        )
        return tenant

    @staticmethod
    def _create_seller_profile(*, user, tenant, phone_number):
        """Create a SellerProfile linking user to tenant."""
        profile = SellerProfile.objects.create(
            user=user,
            tenant=tenant,
            phone_number=phone_number,
        )
        return profile

    @staticmethod
    @transaction.atomic
    def register_seller(*, username, password, tenant_name, phone_number):
        """
        Register a new seller: creates User, Tenant, and SellerProfile
        in a single atomic transaction.
        """
        # 1. Create the user account
        user = AccountService._create_user_account(
            username=username,
            password=password,
        )
        user.role = User.Role.SELLER

        # 2. Create the tenant with user as owner
        tenant = AccountService._create_tenant(
            name=tenant_name,
            owner=user,
        )

        # 3. Link user to tenant and persist role
        user.tenant = tenant
        user.save(update_fields=["role", "tenant"])

        # 4. Create the seller profile
        AccountService._create_seller_profile(
            user=user,
            tenant=tenant,
            phone_number=phone_number,
        )

        return user