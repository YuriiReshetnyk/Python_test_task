"""
Test django custom command for waiting for database.
"""
import pytest
from io import StringIO
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management import call_command
from unittest.mock import patch


@pytest.mark.django_db
@patch('core.management.commands.wait_for_db.connection.ensure_connection')
class TestWaitForDB:
    """Test wait_for_db command."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        out = StringIO()
        call_command('wait_for_db', stdout=out)

        patched_check.assert_called_once()
        assert 'Database unavailable, waiting for 1 second...' \
               not in out.getvalue()
        assert 'Database available!' in out.getvalue()

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        out = StringIO()
        call_command('wait_for_db', stdout=out)

        assert patched_check.call_count == 6
        assert 'Database unavailable, waiting for 1 second...' \
               in out.getvalue()
        assert 'Database available!' in out.getvalue()
