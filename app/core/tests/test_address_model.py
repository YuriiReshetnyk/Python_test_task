"""
Test Address model.
"""
from core.utils import (
    create_external_user,
    create_address
)
from core.constants import DEFAULT_ADDRESS_DATA

import pytest


@pytest.mark.django_db
class TestAddressModel:

    def setup_method(self):
        """Set up an ExternalUser instance for testing."""
        self.user = create_external_user()

    def test_create_address(self):
        """Test creating an address and saving it to database."""
        address = create_address(user=self.user)

        assert address.id is not None
        assert address.user == self.user
        for key, value in DEFAULT_ADDRESS_DATA.items():
            assert getattr(address, key) == value

    def test_create_address_without_user(self):
        """Test creating an address without an external user."""
        address = create_address(user=None)

        assert address.id is not None
        assert address.user is None

    def test_address_user_set_null_after_deleting(self):
        """Test user is set to NULL after user is deleted"""
        address = create_address(user=self.user)

        assert address.user == self.user

        self.user.delete()

        address.refresh_from_db()
        assert address.user is None
