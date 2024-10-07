"""
Admin configuration for the Status model.

This module registers the Status model with the Django admin site using the
StatusModelAdmin class, which currently does not customize any admin behavior.

Classes:
    StatusModelAdmin: Admin configuration for the Status model.

Decorators:
    @register(Status): Registers the Status model with the Django admin site.
"""

from django.contrib.admin import ModelAdmin, register

from illallangi.django.mastodon.models import Status


@register(Status)
class StatusModelAdmin(ModelAdmin):
    """
    StatusModelAdmin is a custom ModelAdmin class for managing Status models in the Django admin interface.

    This class provides customizations and configurations for how Status models are displayed and managed within the Django admin panel.
    Attributes:
        (Add any class attributes here if applicable)
    Methods:
        (Add any methods here if applicable)
    """
