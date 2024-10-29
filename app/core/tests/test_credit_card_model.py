"""
Test CreditCard model.
"""
from core.constants import DEFAULT_CREDIT_CARD_DATA
from core.utils import create_external_user, create_credit_card

import pytest


@pytest.mark.django_db
class TestAddressModel:

    def setup_method(self):
        """Set up an ExternalUser instance for testing."""
        self.user = create_external_user()

    def test_create_credit_card(self):
        """Test creating a credit card and saving it to database."""
        credit_card = create_credit_card(user=self.user)

        assert credit_card.id is not None
        assert credit_card.user is self.user
        for key, value in DEFAULT_CREDIT_CARD_DATA.items():
            assert getattr(credit_card, key) == value

    def test_create_credit_without_user(self):
        """Test creating a credit card
        without user and saving it to database."""
        credit_card = create_credit_card(user=None)

        assert credit_card.id is not None
        assert credit_card.user is None

    def test_credit_card_user_set_null_after_deleting(self):
        """Test credit card user is set to NULL after user is deleted."""
        credit_card = create_credit_card(user=self.user)

        assert credit_card.user == self.user

        self.user.delete()

        credit_card.refresh_from_db()
        assert credit_card.user is None
