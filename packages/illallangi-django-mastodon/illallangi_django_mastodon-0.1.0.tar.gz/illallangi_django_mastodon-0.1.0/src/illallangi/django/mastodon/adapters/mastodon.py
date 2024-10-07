"""MastodonAdapter is a custom adapter for syncing mastodon data using the diffsync library."""

from typing import ClassVar

import diffsync

from illallangi.django.mastodon.diffsyncmodels import Status
from illallangi.django.mastodon.models import Status as DjangoStatus


class MastodonAdapter(diffsync.Adapter):
    """
    MastodonAdapter is an adapter for syncing Status objects from a Django model.

    Attributes:
        Status (class): The Status class to be used for creating Status objects.
        top_level (list): A list containing the top-level object types.
        type (str): The type identifier for this adapter.
    Methods:
        load():
            Loads Status objects from the Django model and adds them to the adapter.
    """

    Status = Status

    top_level: ClassVar = [
        "Status",
    ]

    type = "django_mastodon"

    def load(
        self,
    ) -> None:
        """
        Load all Status objects from the database and adds them to the current instance.

        This method retrieves all instances of the DjangoStatus from the database,
        converts them into Status objects, and adds them to the current instance.
        Returns:
            None
        """
        for obj in DjangoStatus.objects.all():
            self.add(
                Status(
                    pk=obj.pk,
                    url=obj.url,
                    content=obj.content,
                    datetime=obj.datetime.isoformat(),
                ),
            )
