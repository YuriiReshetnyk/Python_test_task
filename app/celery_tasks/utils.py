"""
Store reusable code.
"""
from celery_tasks.exceptions import RetryLaterException
from core import models

import logging
import requests


def fetch_data_from(url):
    """Fetch data from url and raise an error if something is wrong"""
    response = requests.get(url)
    response.raise_for_status()

    if check_retry_later(response):
        raise RetryLaterException("You waited too little "
                                  "before calling API again!")

    return response.json()


def check_retry_later(response):
    """Check if the response indicates to retry later."""
    if "Retry later" in response.text:
        logging.warning("Too little time has passed since "
                        "the last API request! Try again later.")
        return True
    return False


def add_user_to_data(data):
    """Adds user object to data associated with it by uid."""
    user = models.ExternalUser.objects.filter(uid=data['uid']).first()
    data['user'] = user


def save_data(model, data, attributes):
    """Save data to the specified model in the database."""
    extracted_data = extract_attributes(data, attributes)
    instance, created = model.objects.get_or_create(**extracted_data)

    if created:
        logging.info(
            f"{model.__name__} data ({str(instance)}) "
            f"successfully fetched and saved to the database."
        )
    return instance


def extract_attributes(data: dict, valid_keys: list) -> dict:
    """Extract specified attributes from the data."""
    return {key: value for key, value in data.items() if key in valid_keys}
