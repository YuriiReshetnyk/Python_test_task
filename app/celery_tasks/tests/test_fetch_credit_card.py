"""
Test fetching address data from external API.
"""
import pytest
from unittest.mock import patch

import requests
from celery_tasks.tasks.task_fetch_credit_card import (
    task_fetch_credit_card_data
)
from celery_tasks.exceptions import RetryLaterException
from celery_tasks.constants import (
    CREDIT_CARD_API_URL,
    FAKE_CREDIT_CARD_API_RETURN
)
from core import models


@patch("celery_tasks.tasks.task_fetch_credit_card.time.sleep")
@patch("celery_tasks.tasks.task_fetch_credit_card.logging")
@patch('celery_tasks.tasks.task_fetch_credit_card.fetch_data_from')
class TestFetchCreditCard:
    """Test fetching credit card data and saving it to database."""

    @pytest.mark.django_db
    def test_fetch_credit_card_success(self, mock_fetch_data,
                                       mock_logging, mock_sleep):
        """Test successful fetching of credit
        card data and saving it to the database."""
        mock_fetch_data.return_value = FAKE_CREDIT_CARD_API_RETURN

        task_fetch_credit_card_data()

        mock_fetch_data.assert_called_once_with(CREDIT_CARD_API_URL)
        assert models.CreditCard.objects.count() == 1
        mock_logging.info.assert_any_call("Waiting for 3 seconds "
                                          "before fetching data...")
        mock_logging.info.assert_any_call("Fetching credit card data...")
        mock_logging.info.assert_any_call("Credit card is successfully saved")

    def test_fetch_credit_card_http_error(self, mock_fetch_data,
                                          mock_logging, mock_sleep):
        """Test HTTP error reraised during credit card data fetching."""
        mock_fetch_data.side_effect = requests.HTTPError("HTTP error")

        task_fetch_credit_card_data()

        mock_fetch_data.assert_called_once_with(CREDIT_CARD_API_URL)
        mock_logging.error.assert_any_call("HTTP error occurred!")

    def test_fetch_credit_card_request_exception(self, mock_fetch_data,
                                                 mock_logging, mock_sleep):
        """Test request exception reraised
        during credit card data fetching."""
        mock_fetch_data.side_effect = requests.\
            RequestException("Request error")

        task_fetch_credit_card_data()

        mock_fetch_data.assert_called_once_with(CREDIT_CARD_API_URL)
        mock_logging.error.assert_any_call("API request Error!")

    def test_fetch_credit_card_retry_later_exception(self, mock_fetch_data,
                                                     mock_logging, mock_sleep):
        """Test RetryLaterException reraised
        during credit card data fetching."""
        mock_fetch_data.side_effect = RetryLaterException("Retry later")

        task_fetch_credit_card_data()

        mock_fetch_data.assert_called_once_with(CREDIT_CARD_API_URL)
        mock_logging.error.assert_any_call("Don't try so soon!")
