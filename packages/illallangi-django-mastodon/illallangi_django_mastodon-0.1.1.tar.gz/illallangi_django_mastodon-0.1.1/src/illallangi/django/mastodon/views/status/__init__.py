"""
This module initializes the status views for the Django mastodon application.

It imports the `statuses_html` view from the `statuses_html` module and includes it in the `__all__` list for public API exposure.

Modules:
    statuses_html: A view that handles the HTML representation of statuses.

Attributes:
    __all__ (list): A list of public objects of this module, as interpreted by `import *`.
"""

from .status_html import status_html
from .statuses_html import statuses_html

__all__ = [
    "status_html",
    "statuses_html",
]
