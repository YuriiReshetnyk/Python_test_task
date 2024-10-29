"""
Test for reusable code in utils.py
"""
import pytest
from unittest.mock import patch, MagicMock
from celery_tasks.exceptions import RetryLaterException
from celery_tasks import utils
from celery_tasks.constants import USER_ATTRIBUTES
from core.constants import DEFAULT_USER_DATA
from core.utils import create_external_user
from core import models


@patch('celery_tasks.utils.requests.get')
class TestAPI:
    """Tests for functions interacting with external API."""

    def setup_method(self):
        self.mock_response = MagicMock()
        self.mock_response.raise_for_status.return_value = None

    def test_fetch_data_from_success(self, mock_get):
        """Test fetching data successfully from external API."""
        fake_api_data = {
            'id': 1,
            'data': 'Fake data'
        }
        self.mock_response.json.return_value = fake_api_data
        mock_get.return_value = self.mock_response

        result = utils.fetch_data_from("https://example.com/api")
        assert result == fake_api_data
        mock_get.assert_called_once_with("https://example.com/api")

    def test_fetch_data_from_retry_later_exception(self, mock_get):
        """Should raise RetryLaterException if API response indicates retry."""
        self.mock_response.text = "Retry later"
        mock_get.return_value = self.mock_response

        with pytest.raises(RetryLaterException):
            utils.fetch_data_from("https://example.com/api")

        mock_get.assert_called_once_with("https://example.com/api")


@pytest.mark.django_db
class TestDatabaseFunctions:
    """Tests for functions that interact with the database."""

    def setup_method(self):
        """Set up an ExternalUser for tests."""
        self.user = create_external_user()

    def test_add_user_to_data(self):
        """Test adding user to data dictionary."""
        data = {
            "uid": self.user.uid,
            "other_data": "Some other fake data",
        }
        utils.add_user_to_data(data)
        assert data['user'] == self.user

    def test_save_data_creates_instance(self):
        """Test save_data creates a new
        instance if not found in the database."""
        # Create a new user with different uid
        new_user_data = DEFAULT_USER_DATA.copy()
        new_user_data['uid'] = 'fd183feb-3d22-482a-9ac5-1297dbe670ac'
        utils.save_data(models.ExternalUser, new_user_data, USER_ATTRIBUTES)

        assert models.ExternalUser.objects.count() == 2

    def test_save_data_retrieves_existing_instance(self):
        """Test save_data retrieves existing
        instance if it exists in the database."""
        utils.save_data(models.ExternalUser,
                        DEFAULT_USER_DATA,
                        USER_ATTRIBUTES)
        assert models.ExternalUser.objects.count() == 1


class TestBasic:
    """Tests for basic functions"""

    def test_extract_attributes(self):
        """Test extracting specified attributes from the data."""
        data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        attributes = ["key1", "key3"]
        result = utils.extract_attributes(data, attributes)
        assert result == {"key1": "value1", "key3": "value3"}

    def test_check_retry_later(self):
        """Should return True if response indicates retry, otherwise False."""
        mock_retry_response = MagicMock(text="Retry later")
        assert utils.check_retry_later(mock_retry_response) is True

        mock_no_retry_response = MagicMock(text="Something else...")
        assert utils.check_retry_later(mock_no_retry_response) is False
