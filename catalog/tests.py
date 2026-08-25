from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            "name": "Test Product",
            "description": "This is a test product.",
            "price": 10.99,
            "category": 1,  # Assuming category with ID 1 exists
            "brand": 1,     # Assuming brand with ID 1 exists
            "unit": 1       # Assuming unit with ID 1 exists
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

        ######## CREATE TENANT, SELLER PROFILE, ADD NEW RETAILER THEN LIST OUT THE PRODUCCTS, CREATE NEW PRODDUCT