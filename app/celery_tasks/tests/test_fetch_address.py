"""
Test fetching address data from external API.
"""
from celery_tasks.constants import ADDRESS_API_URL, FAKE_ADDRESS_API_RETURN
from celery_tasks.tasks.task_fetch_address import task_fetch_address_data
from celery_tasks.exceptions import RetryLaterException
from core import models
from unittest.mock import patch

import pytest
import requests


@patch("celery_tasks.tasks.task_fetch_address.time.sleep")
@patch("celery_tasks.tasks.task_fetch_address.logging")
@patch('celery_tasks.tasks.task_fetch_address.fetch_data_from')
class TestFetchAddress:
    """Test fetching address data and saving it to database."""

    @pytest.mark.django_db
    def test_fetch_address_success(self, mock_fetch_data,
                                   mock_logging, mock_sleep):
        """Test successful fetching of address
        data and saving it to the database."""
        mock_fetch_data.return_value = FAKE_ADDRESS_API_RETURN

        task_fetch_address_data()

        mock_fetch_data.assert_called_once_with(ADDRESS_API_URL)
        assert models.Address.objects.count() == 1
        mock_logging.info.assert_any_call("Waiting for 3 seconds "
                                          "before fetching data...")
        mock_logging.info.assert_any_call("Fetching address data...")
        mock_logging.info.assert_any_call("Address is successfully saved")

    def test_fetch_address_http_error(self, mock_fetch_data,
                                      mock_logging, mock_sleep):
        """Test HTTP error reraised during address data fetching."""
        mock_fetch_data.side_effect = requests.HTTPError("HTTP error")

        task_fetch_address_data()

        mock_fetch_data.assert_called_once_with(ADDRESS_API_URL)
        mock_logging.error.assert_any_call("HTTP error occurred!")

    def test_fetch_address_request_exception(self, mock_fetch_data,
                                             mock_logging, mock_sleep):
        """Test request exception reraised
        during address data fetching."""
        mock_fetch_data.side_effect = requests.\
            RequestException("Request error")

        task_fetch_address_data()

        mock_fetch_data.assert_called_once_with(ADDRESS_API_URL)
        mock_logging.error.assert_any_call("API request Error!")

    def test_fetch_address_retry_later_exception(self, mock_fetch_data,
                                                 mock_logging, mock_sleep):
        """Test RetryLaterException reraised during address data fetching."""
        mock_fetch_data.side_effect = RetryLaterException("Retry later")

        task_fetch_address_data()

        mock_fetch_data.assert_called_once_with(ADDRESS_API_URL)
        mock_logging.error.assert_any_call("Don't try so soon!")
