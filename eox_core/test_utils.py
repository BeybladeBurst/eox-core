""" Utils for testing"""
from datetime import datetime

import factory
from django.conf import settings as ds
from django.contrib.auth.models import User
from django.test import TestCase

DEFAULT_PASSWORD = 'test'
settings = ds.INTEGRATION_TEST_SETTINGS


class SuperUserFactory(factory.django.DjangoModelFactory):
    """
    A Factory for User objects.
    """
    class Meta:
        """ Meta """
        model = User
        django_get_or_create = ('email', 'username')

    _DEFAULT_PASSWORD = 'test'

    username = factory.Sequence(lambda n: f'robot{n}')
    email = factory.Sequence(lambda n: f'robot+test+{n}@example.com')
    password = factory.PostGenerationMethodCall(
        'set_password', _DEFAULT_PASSWORD)
    first_name = factory.Sequence(lambda n: f'Robot{n}')
    last_name = 'Test'
    is_staff = True
    is_active = True
    is_superuser = True
    last_login = datetime(2012, 1, 1)
    date_joined = datetime(2011, 1, 1)


class TestStorage:
    """
    This is a storage used for testing purposes
    """
    def url(self, name):
        """
        return the name of the asset
        """
        return name


class BaseIntegrationTest(TestCase):
    """
    Base class for the integration test suite.
    """

    def setUp(self):
        """
        Set up the test suite.
        """
        self.default_site = self.get_tenant_data()
        self.tenant_x = self.get_tenant_data("tenant-x")
        self.tenant_y = self.get_tenant_data("tenant-y")
        self.demo_course_id = settings["DEMO_COURSE_ID"]

    def get_tenant_data(self, prefix: str = "") -> dict:
        """
        Get the tenant data.

        If no prefix is provided, the default site data is returned.

        Args:
            prefix (str, optional): The tenant prefix. Defaults to "".

        Returns:
            dict: The tenant data.
        """
        domain = f"{prefix}.{settings['LMS_BASE']}" if prefix else settings["LMS_BASE"]
        return {
            "base_url": f"http://{domain}",
            "domain": domain,
        }
