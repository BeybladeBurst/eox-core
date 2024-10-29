"""Test Middlewares for the EOX Core."""

import requests
from django.conf import settings as ds
from rest_framework import status

from eox_core.test_utils import BaseIntegrationTest

settings = ds.INTEGRATION_TEST_SETTINGS


class TestPathRedirectionMiddleware(BaseIntegrationTest):
    """Integration tests for the PathRedirectionMiddleware."""

    def test_redirect_always(self):
        """Test the redirect_always feature."""
        tenant_x_url = self.tenant_x.get("base_url")

        response = requests.get(f"{tenant_x_url}/courses", timeout=settings["API_TIMEOUT"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.url, f"{tenant_x_url}/about")

        response = requests.get(f"{tenant_x_url}/blog", timeout=settings["API_TIMEOUT"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.url, f"{tenant_x_url}/donate")
