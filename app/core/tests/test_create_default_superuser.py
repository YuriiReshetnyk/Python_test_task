"""
Test django custom command for creating default superuser.
"""
import pytest
from django.core.management import call_command
from django.contrib.auth import get_user_model
from io import StringIO
from unittest.mock import patch
from core.constants import DEFAULT_SUPERUSER_DATA
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
class TestCreateDefaultSuperuser:
    """Test create_default_superuser command."""

    def test_superuser_creation(self):
        """Test that the command creates a superuser if none exists."""
        out = StringIO()
        call_command('create_default_superuser', stdout=out)

        assert User.objects.filter(username='admin').exists()
        assert "Superuser created successfully." in out.getvalue()

    def test_superuser_already_exists(self):
        """Test that no duplicate superuser is created if it already exists."""
        User.objects.create_superuser(**DEFAULT_SUPERUSER_DATA)

        out = StringIO()
        call_command('create_default_superuser', stdout=out)

        assert User.objects.filter(username='admin').count() == 1
        assert "Superuser already exists." in out.getvalue()

    @patch('django.contrib.auth.models.UserManager.create_superuser')
    def test_integrity_error_handling(self, mock_create_superuser):
        """Test that IntegrityError is handled gracefully."""
        mock_create_superuser.side_effect = IntegrityError

        out = StringIO()
        call_command('create_default_superuser', stdout=out)

        assert "Superuser with this username " \
               "or email already exists." in out.getvalue()
