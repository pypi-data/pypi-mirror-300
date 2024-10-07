"""
This module initializes the views for the Django mastodon application.

It imports the `statuses_html` view from the `status` module and includes it in the
`__all__` list to specify the public interface of this module.

Modules:
    status (illallangi.django.mastodon.views.status): Contains the `statuses_html` view.

Attributes:
    __all__ (list): List of public objects of this module, which includes `statuses_html`.
"""

from illallangi.django.mastodon.views.home import home_html
from illallangi.django.mastodon.views.status import status_html, statuses_html

from .favicon import favicon

__all__ = [
    "favicon",
    "home_html",
    "status_html",
    "statuses_html",
]
