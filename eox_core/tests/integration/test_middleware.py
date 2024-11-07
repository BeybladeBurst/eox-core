"""Test Middlewares for the EOX Core."""

import requests
from django.conf import settings as ds
from rest_framework import status

from eox_core.tests.integration.utils import BaseIntegrationTest, get_access_token

settings = ds.INTEGRATION_TEST_SETTINGS

ACCESS_TOKEN = get_access_token()


class TestPathRedirectionMiddleware(BaseIntegrationTest):
    """Integration tests for the PathRedirectionMiddleware."""

    def setUp(self):
        """Setup the test."""
        super().setUp()
        self.tenant_x_url = self.tenant_x.get("base_url")

    def test_without_redirect(self):
        """Test the PathRedirectionMiddleware without any redirection."""
        response = requests.get(f"{self.tenant_x_url}/about", timeout=settings["API_TIMEOUT"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.url, f"{self.tenant_x_url}/about")

    def test_redirect_always(self):
        """Test the redirect_always feature."""
        response = requests.get(f"{self.tenant_x_url}/blog", timeout=settings["API_TIMEOUT"])
        self.assertEqual(response.history[0].status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.url, f"{self.tenant_x_url}/donate")

    def test_login_required(self):
        """Test the login_required feature."""
        response = requests.get(f"{self.tenant_x_url}/tos", timeout=settings["API_TIMEOUT"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.url, f"{self.tenant_x['base_url']}/login?next=/tos")

    def test_not_found(self):
        """Test the not_found feature."""
        response = requests.get(f"{self.tenant_x_url}/privacy", timeout=settings["API_TIMEOUT"])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.url, f"{self.tenant_x_url}/privacy")

    def test_not_found_logged_out(self):
        """Test the not_found and logout feature."""
        response = requests.get(f"{self.tenant_x_url}/contact", timeout=settings["API_TIMEOUT"])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.url, f"{self.tenant_x_url}/contact")

    def test_redirect_logged_out(self):
        """Test the redirect and logout feature."""
        response = requests.get(f"{self.tenant_x_url}/faq", timeout=settings["API_TIMEOUT"])
        self.assertEqual(response.history[0].status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.url, f"{self.tenant_x_url}/donate")
