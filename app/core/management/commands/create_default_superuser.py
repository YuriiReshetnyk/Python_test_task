"""
Django command for creating a default superuser.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from core.constants import DEFAULT_SUPERUSER_DATA


class Command(BaseCommand):
    """Django command to create a default superuser."""

    def handle(self, *args, **options):
        """Create default superuser."""
        if not get_user_model().objects.\
                filter(username=DEFAULT_SUPERUSER_DATA['username']).exists():
            try:
                get_user_model().objects.\
                    create_superuser(**DEFAULT_SUPERUSER_DATA)
                self.stdout.write("Superuser created successfully.")
            except IntegrityError:
                self.stdout.write("Superuser with this username "
                                  "or email already exists.")
        else:
            self.stdout.write("Superuser already exists.")
