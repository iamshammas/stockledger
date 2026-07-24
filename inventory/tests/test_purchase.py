from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from catalog.models import Brand, Category, Product, Unit
from inventory.models import Purchase, PurchaseItem, StockMovement, Supplier
from tenants.models import Tenant


class PurchaseAPITestCase(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="buyer",
			password="secure-password",
			role=User.Role.SELLER,
		)

		self.tenant = Tenant.objects.create(name="Main Tenant", owner=self.user)
		self.user.tenant = self.tenant
		self.user.save(update_fields=["tenant"])

		self.supplier = Supplier.objects.create(
			tenant=self.tenant,
			name="Acme Supplies",
			phone="1234567890",
		)

		self.category = Category.objects.create(
			tenant=self.tenant,
			name="Beverages",
		)
		self.brand = Brand.objects.create(
			tenant=self.tenant,
			name="FreshCo",
		)
		self.unit = Unit.objects.create(
			tenant=self.tenant,
			name="Bottle",
			short_code="btl",
		)
		self.product = Product.objects.create(
			tenant=self.tenant,
			name="Sparkling Water",
			category=self.category,
			brand=self.brand,
			unit=self.unit,
			sku="SW-001",
			current_selling_price=Decimal("6.00"),
		)

	def test_authenticated_user_can_create_purchase(self):
		refresh = RefreshToken.for_user(self.user)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

		payload = {
			"supplier": self.supplier.id,
			"purchase_date": "2026-07-24",
			"notes": "Initial stock",
			"items": [
				{
					"product": self.product.id,
					"quantity": "5.000",
					"buying_price": "4.50",
					"selling_price": "6.00",
				}
			],
		}

		response = self.client.post("/api/inventory/purchases/", payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Purchase.objects.count(), 1)
		self.assertEqual(PurchaseItem.objects.count(), 1)
		self.assertEqual(StockMovement.objects.count(), 1)

		purchase = Purchase.objects.get()
		self.assertEqual(purchase.total_amount, Decimal("22.50"))
		self.assertEqual(purchase.supplier, self.supplier)
		self.assertEqual(purchase.recorded_by, self.user)
