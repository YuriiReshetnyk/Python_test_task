"""
Database models.
"""
from django.db import models


class ExternalUser(models.Model):
    """User information from external APIs."""
    uid = models.CharField(max_length=36, unique=True)
    password = models.CharField(max_length=31)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    avatar = models.URLField(max_length=255)
    gender = models.CharField(max_length=31)
    phone_number = models.CharField(max_length=50)
    social_insurance_number = models.CharField(max_length=9)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CreditCard(models.Model):
    """Credit Card of the external user."""
    credit_card_number = models.CharField(max_length=19)
    credit_card_expiry_date = models.DateField()
    credit_card_type = models.CharField(max_length=30)
    user = models.ForeignKey(
        ExternalUser,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.credit_card_number


class Address(models.Model):
    """Address of the external user."""
    city = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    secondary_address = models.CharField(max_length=255)
    building_number = models.CharField(max_length=255)
    mail_box = models.CharField(max_length=255)
    community = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    time_zone = models.CharField(max_length=255)
    street_suffix = models.CharField(max_length=255)
    city_suffix = models.CharField(max_length=255)
    city_prefix = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    state_abbr = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    full_address = models.CharField(max_length=255)
    user = models.ForeignKey(
        ExternalUser,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.full_address

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
