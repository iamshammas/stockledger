from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from tenants.models import Tenant
from accounts.models import User
from customers.models import Retailer

class RetailerAPITest(APITestCase):

    def setUp(self):
        # Create owner first (without a tenant)
        self.owner = User.objects.create_user(
            username="owner",
            password="owner123",
            role=User.Role.SUPER_ADMIN,
        )
        # Create a tenant and associate it with the owner
        self.tenant = Tenant.objects.create(name="Test Tenant", owner=self.owner)

        # Assign tenant to owner
        self.owner.tenant = self.tenant
        self.owner.save()

        # Create a seller user and associate it with the tenant
        self.user = User.objects.create_user(
            username="seller",
            password="test123",
            tenant=self.tenant,
            role=User.Role.SELLER
        )
        self.client.force_authenticate(user=self.user)

        self.url = reverse("retailer-list")

    def test_create_retailer(self):
        data = {
            "retailer_name": "ABC Stores",
            "shop_name": "ABC Shop",
            "phone": "9876543210",
            "email": "abc@test.com",
            "address": "Kannur",
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Retailer.objects.count(), 1)
        retailer = Retailer.objects.first()
        self.assertEqual(retailer.retailer_name, "ABC Stores")
        self.assertEqual(retailer.tenant, self.tenant)
        self.assertEqual(retailer.phone, "9876543210")