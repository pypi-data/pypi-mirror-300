"""
Status represents a mastodon activity with details such as date, laps, distance, and URL.

Attributes:
    pk: The primary key for the model.
    url: A URL related to the mastodon activity.
    content: The content of the mastodon activity.
    datetime: The datetime of the mastodon activity.

Methods:
    __str__(): Returns a string representation of the Status instance in the format "Status {id}".
"""

import diffsync

from illallangi.django.mastodon.models.status import Status as ModelStatus


class Status(
    diffsync.DiffSyncModel,
):
    """
    Status represents a mastodon activity with specific details such as date, laps, distance, and URL.

    Attributes:
        pk: The primary key for the model.
        url: A URL related to the mastodon activity.
        content: The content of the mastodon activity.
        datetime: The datetime of the mastodon activity.
    Methods:
        __str__(): Returns a string representation of the Status instance in the format "Status {id}".
    """

    pk: int
    url: str
    content: str
    datetime: str

    _modelname = "Status"
    _identifiers = ("url",)
    _attributes = (
        "content",
        "datetime",
    )

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Status":
        """
        Create a Status instance.

        This method updates or creates a Status object using the provided ids and attrs,
        then creates a Status instance with the updated or created Status object's
        primary key and the provided ids and attrs.
        Args:
            cls: The class that this method is called on.
            adapter: The adapter to use for creating the Status instance.
            ids (dict): A dictionary containing the identifiers for the Status object.
            attrs (dict): A dictionary containing the attributes for the Status object.
        Returns:
            Status: The created Status instance.
        """
        obj = ModelStatus.objects.update_or_create(
            url=ids["url"],
            defaults={
                "content": attrs["content"],
                "datetime": attrs["datetime"],
            },
        )[0]

        return super().create(
            adapter,
            {
                "pk": obj.pk,
                **ids,
            },
            attrs,
        )

    def update(
        self,
        attrs: dict,
    ) -> "Status":
        """
        Update the current Status instance with the provided attributes.

        Args:
            attrs (dict): A dictionary of attributes to update the instance with.
        Returns:
            Status: The updated Status instance.
        """
        ModelStatus.objects.filter(
            pk=self.pk,
        ).update(
            **attrs,
        )

        return super().update(attrs)

    def delete(
        self,
    ) -> "Status":
        """
        Delete the current Status instance from the database.

        This method first deletes the associated Status object using its primary key (pk),
        and then calls the superclass's delete method to remove the Status instance.
        Returns:
            Status: The deleted Status instance.
        """
        ModelStatus.objects.get(
            pk=self.pk,
        ).delete()

        return super().delete()
