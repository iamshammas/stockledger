from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
User = get_user_model()

class JWTLoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_login_with_valid_credentials(self):
        url = "/api/auth/login/"
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)  
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):
        url = "/api/auth/login/"
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_login_with_missing_fields(self):
        url = "/api/auth/login/"
        data = {"username": "testuser"}  
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)

class RefreshTokenTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        url = "/api/auth/login/"
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.refresh_token = response.data["refresh"]

    def test_refresh_token_with_valid_token(self):
        url = "/api/auth/refresh/"
        data = {"refresh": self.refresh_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_refresh_token_with_invalid_token(self):
        url = "/api/auth/refresh/"
        data = {"refresh": "invalidtoken"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_refresh_token_with_missing_fields(self):
        url = "/api/auth/refresh/"
        data = {}  
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)