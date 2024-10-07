"""
Admin configuration for the Swim model.

This module registers the Swim model with the Django admin site using the
SwimModelAdmin class, which currently does not customize any admin behavior.

Classes:
    SwimModelAdmin: Admin configuration for the Swim model.

Decorators:
    @register(Swim): Registers the Swim model with the Django admin site.
"""

from django.contrib.admin import ModelAdmin, register

from illallangi.django.swimming.models import Swim


@register(Swim)
class SwimModelAdmin(ModelAdmin):
    """
    SwimModelAdmin is a custom ModelAdmin class for managing Swim models in the Django admin interface.

    This class provides customizations and configurations for how Swim models are displayed and managed within the Django admin panel.
    Attributes:
        (Add any class attributes here if applicable)
    Methods:
        (Add any methods here if applicable)
    """
