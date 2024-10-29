"""
Task fetching credit card data.
"""
import time

from celery_tasks.constants import CREDIT_CARD_ATTRIBUTES, CREDIT_CARD_API_URL
from celery_tasks.exceptions import RetryLaterException
from celery import shared_task
from core import models
from celery_tasks.utils import (
    save_data,
    fetch_data_from,
    add_user_to_data
)

import requests
import logging

logging.basicConfig(level=logging.INFO)


@shared_task
def task_fetch_credit_card_data():
    """Fetch credit card data from external API and save it to database."""
    try:
        logging.info("Waiting for 3 seconds before fetching data...")
        time.sleep(3)
        logging.info("Fetching credit card data...")
        data = fetch_data_from(CREDIT_CARD_API_URL)

    except requests.HTTPError:
        logging.error("HTTP error occurred!")
    except requests.RequestException:
        logging.error("API request Error!")
    except RetryLaterException:
        logging.error("Don't try so soon!")
    else:
        save_credit_card_data(data)
        logging.info("Credit card is successfully saved")


def save_credit_card_data(data):
    """Save the address data to the database."""
    add_user_to_data(data)
    save_data(models.CreditCard, data, CREDIT_CARD_ATTRIBUTES)
