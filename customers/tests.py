from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from customers.models import Retailer
from tenants.models import Tenant


class RetailerAPITestCase(APITestCase):
	def setUp(self):
		self.user_a = User.objects.create_user(
			username="tenant-a-user",
			password="secure-password",
			role=User.Role.SELLER,
		)
		self.tenant_a = Tenant.objects.create(name="Tenant A", owner=self.user_a)
		self.user_a.tenant = self.tenant_a
		self.user_a.save(update_fields=["tenant"])

		self.user_b = User.objects.create_user(
			username="tenant-b-user",
			password="secure-password",
			role=User.Role.SELLER,
		)
		self.tenant_b = Tenant.objects.create(name="Tenant B", owner=self.user_b)
		self.user_b.tenant = self.tenant_b
		self.user_b.save(update_fields=["tenant"])

		self.retailers_url = "/api/customers/retailers/"

	def authenticate(self, user):
		refresh = RefreshToken.for_user(user)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

	def create_retailer(self, *, tenant, retailer_name, phone):
		return Retailer.objects.create(
			tenant=tenant,
			retailer_name=retailer_name,
			phone=phone,
			shop_name="",
			email="",
			address="",
			credit_balance=Decimal("0.00"),
			is_active=True,
		)

	def test_create_retailer(self):
		self.authenticate(self.user_a)

		payload = {
			"retailer_name": "Retailer One",
			"shop_name": "Main Shop",
			"phone": "1234567890",
			"email": "retailer@example.com",
			"address": "123 Market Street",
			"credit_balance": "0.00",
			"is_active": True,
		}

		response = self.client.post(self.retailers_url, payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Retailer.objects.count(), 1)

		retailer = Retailer.objects.get()
		self.assertEqual(retailer.tenant, self.tenant_a)

	def test_list_retailers_is_tenant_scoped(self):
		self.create_retailer(tenant=self.tenant_a, retailer_name="A One", phone="1111111111")
		self.create_retailer(tenant=self.tenant_a, retailer_name="A Two", phone="2222222222")
		self.create_retailer(tenant=self.tenant_b, retailer_name="B One", phone="3333333333")

		self.authenticate(self.user_a)

		response = self.client.get(self.retailers_url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 2)

	def test_duplicate_phone_same_tenant_is_rejected(self):
		self.authenticate(self.user_a)

		payload = {
			"retailer_name": "Retailer One",
			"shop_name": "Main Shop",
			"phone": "9876543210",
			"email": "retailer1@example.com",
			"address": "123 Market Street",
			"credit_balance": "0.00",
			"is_active": True,
		}

		first_response = self.client.post(self.retailers_url, payload, format="json")
		self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

		duplicate_response = self.client.post(self.retailers_url, payload, format="json")

		self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Retailer.objects.count(), 1)

	def test_same_phone_across_tenants_is_allowed(self):
		self.authenticate(self.user_a)

		payload_a = {
			"retailer_name": "Retailer A",
			"shop_name": "Shop A",
			"phone": "9876543210",
			"email": "reta@example.com",
			"address": "Address A",
			"credit_balance": "0.00",
			"is_active": True,
		}
		response_a = self.client.post(self.retailers_url, payload_a, format="json")
		self.assertEqual(response_a.status_code, status.HTTP_201_CREATED)

		self.authenticate(self.user_b)
		payload_b = {
			"retailer_name": "Retailer B",
			"shop_name": "Shop B",
			"phone": "9876543210",
			"email": "retb@example.com",
			"address": "Address B",
			"credit_balance": "0.00",
			"is_active": True,
		}
		response_b = self.client.post(self.retailers_url, payload_b, format="json")

		self.assertEqual(response_b.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Retailer.objects.count(), 2)
