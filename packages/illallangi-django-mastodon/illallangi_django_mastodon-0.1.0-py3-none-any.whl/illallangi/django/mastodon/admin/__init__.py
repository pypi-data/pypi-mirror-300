"""
This module initializes the admin interface for the mastodon application.

It imports the StatusModelAdmin class from the status module and includes it in the
__all__ list to specify the public API of this module.

Classes:
    StatusModelAdmin: Admin interface for the Status model.
"""

from .status import StatusModelAdmin

__all__ = [
    "StatusModelAdmin",
]
