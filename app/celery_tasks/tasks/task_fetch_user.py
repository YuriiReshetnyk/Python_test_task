"""
Task fetching user data.
"""
import time

from celery_tasks.constants import USER_ATTRIBUTES, USER_API_URL
from celery_tasks.exceptions import RetryLaterException
from celery import shared_task
from core import models
from celery_tasks.utils import (
    save_data,
    fetch_data_from,
)
import requests
import logging

logging.basicConfig(level=logging.INFO)


@shared_task
def task_fetch_user_data():
    """Fetch user data from external API and save it to database."""
    try:
        logging.info("Waiting for 3 seconds before fetching data...")
        time.sleep(3)
        logging.info("Fetching user data...")
        data = fetch_data_from(USER_API_URL)

    except requests.HTTPError:
        logging.error("HTTP error occurred!")
    except requests.RequestException:
        logging.error("API request Error!")
    except RetryLaterException:
        logging.error("Don't try so soon!")
    else:
        user = save_user_data(data)
        associate_other_info(user, data)
        logging.info("User is successfully saved")


def save_user_data(data):
    """Save user data to database"""
    return save_data(models.ExternalUser, data, USER_ATTRIBUTES)


def associate_other_info(user, data):
    """Associate other user information
    about user with him if it is in database."""
    associate_address(user, data['address']['coordinates'])
    associate_credit_card(user, data['credit_card']['cc_number'])


def associate_address(user, coordinates):
    """Associate address with user if it exists."""
    attributes = {
        'latitude': coordinates['lat'],
        'longitude': coordinates['lng']
    }
    associate_with_user(user, models.Address, **attributes)


def associate_with_user(user, model, **attributes):
    """Associate model object with attributes to user if it exits."""
    if model.objects.filter(**attributes).exists():
        instance = model.objects.get(**attributes)
        instance.user = user
        instance.save()
        logging.info(f"Associated {model.__name__} "
                     f"with id={instance.id} to user ({str(user)}).")


def associate_credit_card(user, credit_card_number):
    """Associate credit card with user if it exists."""
    attributes = {
        'credit_card_number': credit_card_number
    }
    associate_with_user(user, models.CreditCard, **attributes)
