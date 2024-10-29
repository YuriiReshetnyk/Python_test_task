"""
Test Address admin page.
"""
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

from core.utils import create_address

import pytest


@pytest.mark.django_db
class TestAdminPages:

    def setup_method(self):
        """Set up client for tests."""
        self.client = Client()
        self.superuser = get_user_model().objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.client.force_login(user=self.superuser)

    def test_address_list(self):
        """Test that addresses are listed on page."""
        address = create_address()
        response = self.client.get(reverse('admin:core_address_changelist'))

        assert response.status_code == 200
        assert address.full_address in str(response.content)

    def test_create_address_page(self):
        """Test the create address page works."""
        url = reverse('admin:core_address_add')
        response = self.client.get(url)

        assert response.status_code == 200

    def test_edit_address_page(self):
        """Test the edit address page works."""
        address = create_address()
        url = reverse('admin:core_address_change', args=[address.id])
        response = self.client.get(url)

        assert response.status_code == 200
