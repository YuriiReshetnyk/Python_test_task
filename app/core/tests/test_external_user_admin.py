"""
Test ExternalUser admin page.
"""
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

from core.utils import create_external_user

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

    def test_external_user_list(self):
        """Test that external users are listed on page."""
        user = create_external_user()

        url = reverse('admin:core_externaluser_changelist')
        response = self.client.get(url)

        assert response.status_code == 200
        assert user.username in str(response.content)
        assert user.first_name in str(response.content)
        assert user.last_name in str(response.content)

    def test_create_external_user_page(self):
        """Test the create external user page works."""
        url = reverse('admin:core_externaluser_add')
        response = self.client.get(url)

        assert response.status_code == 200

    def test_edit_external_user_page(self):
        """Test the edit external user page works."""
        user = create_external_user()
        url = reverse('admin:core_externaluser_change', args=[user.id])
        response = self.client.get(url)

        assert response.status_code == 200
