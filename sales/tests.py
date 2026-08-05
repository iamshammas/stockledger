from django.urls import reverse
from rest_framework import response
from rest_framework.test import APITestCase

from accounts.models import User
from catalog.models import Brand, Category, Product, Unit
from customers.models import Retailer
from inventory.models import Purchase, PurchaseItem, Supplier
from tenants.models import Tenant

from datetime import date

from sales.models import Sale

class SaleAPITest(APITestCase):

    def setUp(self):
        # Create owner first (without a tenant)
        self.owner = User.objects.create_user(
            username="owner",
            password="owner123",
            role=User.Role.SUPER_ADMIN,
        )
        # Create a tenant and associate it with the owner
        self.tenant = Tenant.objects.create(name="Test Tenant", owner=self.owner)
        self.owner.tenant = self.tenant
        self.owner.save()
        self.user = User.objects.create_user(
            username="seller",
            password="test123",
            tenant=self.tenant,
            role=User.Role.SELLER
        )

        self.client.force_authenticate(user=self.user)
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
            current_selling_price=6.00,
        )
        self.retailer = Retailer.objects.create(
            tenant=self.tenant,
            retailer_name="ABC Stores",
            shop_name="ABC Shop",
            phone="9876543210",
            email="abc@store.com"
        )
        self.url = reverse("sale-list")

    def test_fifo_sale_spans_multiple_purchase_batches(self):
        # Create a supplier
        supplier = Supplier.objects.create(
            tenant=self.tenant,
            name="Acme Supplies",
            phone="1234567890",
        )

        purchase1 = Purchase.objects.create(
            tenant=self.tenant,
            supplier=supplier,
            recorded_by=self.user,
            purchase_date="2026-07-24",
        )

        purchase_item1 = PurchaseItem.objects.create(
            purchase=purchase1,
            product=self.product,
            quantity=10,
            buying_price=5.00,
            selling_price=6.00,
            remaining_quantity=10,
        )

        purchase2 = Purchase.objects.create(
            tenant=self.tenant,
            supplier=supplier,
            purchase_date="2026-07-25",
            recorded_by=self.user,
        )
        purchase_item2 = PurchaseItem.objects.create(
            purchase=purchase2,
            product=self.product,
            quantity=20,
            buying_price=4.50,
            selling_price=6.00,
            remaining_quantity=20,
        )

        payload = {
            "retailer": self.retailer.id,
            "invoice_date": date.today(),
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 20,
                    "selling_price": 150,
                }
            ]
        }

        response = self.client.post(self.url, payload, format="json")
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, 201)
