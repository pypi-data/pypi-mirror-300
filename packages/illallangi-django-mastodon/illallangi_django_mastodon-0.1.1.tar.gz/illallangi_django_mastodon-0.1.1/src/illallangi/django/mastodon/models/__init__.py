"""
This module initializes the models package and imports the Status model.

Classes:
    Status: Represents a mastodon model.

__all__:
    List of public objects of this module, as interpreted by import *.
"""

from .status import Status

__all__ = [
    "Status",
]
