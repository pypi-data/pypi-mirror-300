"""Status represents a mastodon activity with details such as datetime, content, and URL."""

from django.db import models
from django.urls import reverse
from django_sqids import SqidsField


class Status(
    models.Model,
):
    """
    Status represents a mastodon activity with specific details such as datetime, content, and URL.

    Attributes:
        id (AutoField): The primary key for the model.
        url (URLField): A URL related to the mastodon activity.
        content (TextField): The content of the mastodon activity.
        datetime (DateTimeField): The datetime of the mastodon activity.
    Methods:
        __str__(): Returns a string representation of the Status instance in the format "Status {id}".
    """

    # Surrogate Keys

    id = models.AutoField(
        primary_key=True,
    )

    sqid = SqidsField(
        real_field_name="id",
        min_length=6,
    )

    # Fields

    url = models.URLField(
        null=False,
        blank=False,
        unique=True,
    )

    content = models.TextField(
        null=False,
        blank=False,
    )

    datetime = models.DateTimeField(
        null=False,
        blank=False,
    )

    # Methods

    def __str__(
        self,
    ) -> str:
        """
        Return a string representation of the Status instance.

        Returns:
            str: A string in the format "Status {id}" where {id} is the ID of the Status instance.
        """
        return f"Status {self.id}"

    def get_absolute_url(
        self,
    ) -> str:
        """
        Return the absolute URL of the Status instance.

        Returns:
            str: The absolute URL of the Status instance.
        """
        return reverse(
            "mastodon:status_html",
            kwargs={
                "status_slug": self.sqid,
                "status_year": str(self.datetime.year).zfill(4),
                "status_month": str(self.datetime.month).zfill(2),
                "status_day": str(self.datetime.day).zfill(2),
            },
        )
