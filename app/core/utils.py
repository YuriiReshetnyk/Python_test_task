"""
Reusable code.
"""
from core.constants import (
    DEFAULT_USER_DATA,
    DEFAULT_ADDRESS_DATA,
    DEFAULT_CREDIT_CARD_DATA,
)
from core import models


def create_external_user(**custom_attributes):
    """Create and return an external user."""
    attributes = DEFAULT_USER_DATA.copy()
    update_dictionary_values(attributes, custom_attributes)
    return models.ExternalUser.objects.create(**attributes)


def update_dictionary_values(default_dict: dict, new_values: dict) -> None:
    for key, value in new_values.items():
        default_dict[key] = value


def create_credit_card(user=None, **custom_attributes):
    """Create and return a credit card for a user."""
    attributes = DEFAULT_CREDIT_CARD_DATA.copy()
    update_dictionary_values(attributes, custom_attributes)
    return models.CreditCard.objects.create(user=user, **attributes)


def create_address(user=None, **custom_attributes):
    """Create and return an address for a user."""
    attributes = DEFAULT_ADDRESS_DATA.copy()
    update_dictionary_values(attributes, custom_attributes)
    return models.Address.objects.create(user=user, **attributes)
