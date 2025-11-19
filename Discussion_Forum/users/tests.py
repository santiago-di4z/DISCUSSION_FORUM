from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

class AuthTests(TestCase):

    # Test --> User Registration
    def test_user_reg(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "12345678",
            "password2": "12345678",
        }

        response = self.client.post(url, data, follow=True)

        # User created
        self.assertTrue(User.objects.filter(username="testuser").exists())

        # User automatically logged in
        self.assertTrue(response.context["user"].is_authenticated)

    # Test --> User Login
    def test_user_lin(self):
        # Create test user
        User.objects.create_user(username="user", password="pass1234")

        url = reverse('login')
        data = {
            "username": "user",
            "password": "pass1234",
        }

        response = self.client.post(url, data, follow=True)

        # Login exitoso
        self.assertTrue(response.context["user"].is_authenticated)

    # Test --> Log in with wrong credentials
    def test_user_wrong_lin(self):
        url = reverse('login')
        data = {
            "username": "fake",
            "password": "wrongpass",
        }

        response = self.client.post(url, data)

        # Login fails -> user NOT authenticated
        self.assertFalse(response.context["user"].is_authenticated)

    # Test --> User Logout
    def test_user_lout(self):
        # Create and log in user
        user = User.objects.create_user(username="u", password="p12345")
        self.client.login(username="u", password="p12345")

        url = reverse('logout')
        response = self.client.get(url, follow=True)

        # Successful logout
        self.assertFalse(response.context["user"].is_authenticated)

    # Test --> Register redirects to home
    def test_reg_to_home(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "abcd1234",
            "password2": "abcd1234",
        }

        response = self.client.post(url, data, follow=True)

        # Redirects to home
        self.assertEqual(response.redirect_chain[-1][1], 302)
