"""
Test ExternalUser model.
"""
from core.constants import DEFAULT_USER_DATA
from core.utils import create_external_user
from django.db.utils import IntegrityError

import pytest


@pytest.mark.django_db
class TestExternalUserModel:

    def test_create_external_user(self):
        """Test creating an ExternalUser instance
        and saving it to the database."""
        user = create_external_user()

        assert user.id is not None
        for key, value in DEFAULT_USER_DATA.items():
            assert getattr(user, key) == value

    def test_uid_uniqueness(self):
        """Test that the UID field is unique for each ExternalUser."""
        user = create_external_user()

        with pytest.raises(IntegrityError):
            create_external_user(uid=user.uid)
