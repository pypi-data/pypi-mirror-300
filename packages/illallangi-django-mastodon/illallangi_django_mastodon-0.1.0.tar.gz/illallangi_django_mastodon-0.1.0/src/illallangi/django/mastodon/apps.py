"""
This module defines the configuration for the 'mastodon' Django application.

Classes:
    MastodonConfig(AppConfig): Configuration class for the 'mastodon' app.
"""

from django.apps import AppConfig


class MastodonConfig(AppConfig):
    """
    Django application configuration for the Mastodon app.

    Attributes:
        default_auto_field (str): Specifies the type of auto-incrementing primary key to use for models in this app.
        name (str): The full Python path to the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "illallangi.django.mastodon"
