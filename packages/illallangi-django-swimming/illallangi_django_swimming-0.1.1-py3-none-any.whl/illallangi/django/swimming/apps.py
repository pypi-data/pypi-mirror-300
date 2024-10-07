"""
This module defines the configuration for the 'swimming' Django application.

Classes:
    SwimmingConfig(AppConfig): Configuration class for the 'swimming' app.
"""

from django.apps import AppConfig


class SwimmingConfig(AppConfig):
    """
    Django application configuration for the Swimming app.

    Attributes:
        default_auto_field (str): Specifies the type of auto-incrementing primary key to use for models in this app.
        name (str): The full Python path to the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "illallangi.django.swimming"
