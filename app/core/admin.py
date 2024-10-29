"""
Django admin customization.
"""
from django.contrib import admin

from core import models


class ExternalUserAdmin(admin.ModelAdmin):
    """Define the admin pages for external users."""
    ordering = ["id"]
    list_display = ["username", "first_name", "last_name"]
    list_filter = ["gender"]
    exclude = ('id',)


class AddressAdmin(admin.ModelAdmin):
    """Define the admin pages for addresses."""
    ordering = ["id"]
    list_display = ["user", "full_address"]
    list_filter = ["country", "time_zone"]
    exclude = ('id',)


class CreditCardAdmin(admin.ModelAdmin):
    """Define the admin pages for credit cards."""
    ordering = ["id"]
    list_display = ["user", "credit_card_number", "credit_card_type"]
    list_filter = ["credit_card_type"]
    exclude = ('id',)


admin.site.register(models.ExternalUser, ExternalUserAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.CreditCard, CreditCardAdmin)
