"""
Command to synchronize mastodon data from one adapter to another.

This command uses the MastodonMastodonAdapter as the source and the
DjangoMastodonAdapter as the destination. It loads data from the source
adapter and synchronizes it to the destination adapter.

Attributes:
    help (str): Description of the command.
    requires_migrations_checks (bool): Indicates if migration checks are required.

Methods:
    handle(*args, **kwargs):
        Executes the synchronization process by loading data from the source
        adapter and synchronizing it to the destination adapter. Outputs a
        success message upon completion.
"""

from django.core.management.base import BaseCommand

from illallangi.django.mastodon.adapters import MastodonAdapter as DjangoMastodonAdapter
from illallangi.mastodon.adapters import MastodonAdapter as MastodonMastodonAdapter


class Command(BaseCommand):
    """
    Command to sync mastodon data from one adapter to another.

    This command uses the MastodonMastodonAdapter as the source and the
    DjangoMastodonAdapter as the destination. It loads data from the source
    adapter, loads data from the destination adapter, and then synchronizes
    the data from the source to the destination.
    Attributes:
        help (str): Description of the command.
        requires_migrations_checks (bool): Indicates if migration checks are required.
    Methods:
        handle(*args, **kwargs):
            Executes the synchronization process. Loads data from the source
            adapter, loads data from the destination adapter, and synchronizes
            the data from the source to the destination. Outputs a success message
            upon completion.
    """

    help = "Sync Mastodon data from one adapter to another."
    requires_migrations_checks = True

    def handle(
        self,
        *_args: tuple,
        **_kwargs: dict,
    ) -> None:
        """
        Handle the synchronization process between the MastodonMastodonAdapter and DjangoMastodonAdapter.

        This method performs the following steps:
        1. Initializes the source adapter (MastodonMastodonAdapter).
        2. Initializes the destination adapter (DjangoMastodonAdapter).
        3. Loads data from the source adapter.
        4. Loads data from the destination adapter.
        5. Synchronizes data from the source adapter to the destination adapter.
        6. Outputs a success message upon completion.
        Args:
            *_args (tuple): Positional arguments (not used).
            **_kwargs (dict): Keyword arguments (not used).
        Returns:
            None
        """
        src = MastodonMastodonAdapter()
        dst = DjangoMastodonAdapter()

        src.load()
        dst.load()

        src.sync_to(dst)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully synchronised.",
            ),
        )
