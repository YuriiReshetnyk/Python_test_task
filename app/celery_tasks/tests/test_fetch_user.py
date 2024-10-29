"""
Test fetching user data from external API.
"""
from unittest.mock import patch
from core import models
from celery_tasks.tasks.task_fetch_user import (
    task_fetch_user_data,
    save_user_data,
    associate_with_user
)
from celery_tasks.exceptions import RetryLaterException
from celery_tasks.utils import save_data
from celery_tasks.constants import (
    USER_API_URL,
    FAKE_USER_API_RETURN,
    FAKE_ADDRESS_API_RETURN,
    ADDRESS_ATTRIBUTES
)
import requests
import pytest


def create_address(coordinates: dict) -> models.Address:
    """Create and return Address object with specific coordinates."""
    address_data = FAKE_ADDRESS_API_RETURN.copy()
    address_data['latitude'] = coordinates['latitude']
    address_data['longitude'] = coordinates['longitude']

    return save_data(models.Address, address_data, ADDRESS_ATTRIBUTES)


@patch('celery_tasks.tasks.task_fetch_user.time.sleep')
@patch('celery_tasks.tasks.task_fetch_user.logging')
@patch('celery_tasks.tasks.task_fetch_user.fetch_data_from')
class TestFetchUser:
    """Test fetching user data and saving it to the database."""

    @pytest.mark.django_db
    def test_fetch_user_success(self, mock_fetch_data,
                                mock_logging, mock_sleep):
        """Test successful fetching of user
        data and saving it to the database."""
        mock_fetch_data.return_value = FAKE_USER_API_RETURN

        task_fetch_user_data()

        mock_fetch_data.assert_called_once_with(USER_API_URL)
        assert models.ExternalUser.objects.count() == 1
        mock_logging.info.assert_any_call("Waiting for 3 seconds "
                                          "before fetching data...")
        mock_logging.info.assert_any_call("Fetching user data...")
        mock_logging.info.assert_any_call("User is successfully saved")

    def test_fetch_user_http_error(self, mock_fetch_data,
                                   mock_logging, mock_sleep):
        """Test HTTP error raised during user data fetching."""
        mock_fetch_data.side_effect = requests.HTTPError("HTTP error")

        task_fetch_user_data()

        mock_fetch_data.assert_called_once_with(USER_API_URL)
        mock_logging.error.assert_any_call("HTTP error occurred!")

    def test_fetch_user_request_exception(self, mock_fetch_data,
                                          mock_logging, mock_sleep):
        """Test request exception raised during user data fetching."""
        mock_fetch_data.side_effect = requests.\
            RequestException("Request error")

        task_fetch_user_data()

        mock_fetch_data.assert_called_once_with(USER_API_URL)
        mock_logging.error.assert_any_call("API request Error!")

    def test_fetch_user_retry_later_exception(self, mock_fetch_data,
                                              mock_logging, mock_sleep):
        """Test RetryLaterException raised during credit card data fetching."""
        mock_fetch_data.side_effect = RetryLaterException("Retry later")

        task_fetch_user_data()

        mock_fetch_data.assert_called_once_with(USER_API_URL)
        mock_logging.error.assert_any_call("Don't try so soon!")

    @pytest.mark.django_db
    def test_associate_with_user(self, mock_fetch_data,
                                 mock_logging, mock_sleep):
        """Test associate user with address that has the same coordinates."""
        user = save_user_data(FAKE_USER_API_RETURN)

        user_coordinates = {
            'latitude': FAKE_USER_API_RETURN['address']['coordinates']['lat'],
            'longitude': FAKE_USER_API_RETURN['address']['coordinates']['lng']
        }
        address = create_address(user_coordinates)
        associate_with_user(user, models.Address, **user_coordinates)

        address.refresh_from_db()
        assert address.user == user
