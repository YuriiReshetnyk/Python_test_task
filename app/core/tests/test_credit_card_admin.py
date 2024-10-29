"""
Test CreditCard admin page.
"""
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

from core.utils import create_credit_card

import pytest


@pytest.mark.django_db
class TestCreditCardAdmin:

    def setup_method(self):
        """Set up client for tests."""
        self.client = Client()
        self.superuser = get_user_model().objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.client.force_login(user=self.superuser)

    def test_credit_card_list(self):
        """Test that credit cards are listed on page."""
        credit_card = create_credit_card()
        response = self.client.get(reverse('admin:core_creditcard_changelist'))

        assert response.status_code == 200
        assert credit_card.credit_card_number in str(response.content)
        assert credit_card.credit_card_type in str(response.content)

    def test_create_credit_card_page(self):
        """Test the create credit card page works."""
        url = reverse('admin:core_creditcard_add')
        response = self.client.get(url)

        assert response.status_code == 200

    def test_edit_credit_card_page(self):
        """Test the edit credit card page works."""
        credit_card = create_credit_card()
        url = reverse('admin:core_creditcard_change', args=[credit_card.id])
        response = self.client.get(url)

        assert response.status_code == 200
