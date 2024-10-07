"""
Command to synchronize swimming data from one adapter to another.

This command uses the MastodonSwimmingAdapter as the source and the
DjangoSwimmingAdapter as the destination. It loads data from the source
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

from illallangi.django.swimming.adapters import SwimmingAdapter as DjangoSwimmingAdapter
from illallangi.mastodon.adapters import SwimmingAdapter as MastodonSwimmingAdapter


class Command(BaseCommand):
    """
    Command to sync swimming data from one adapter to another.

    This command uses the MastodonSwimmingAdapter as the source and the
    DjangoSwimmingAdapter as the destination. It loads data from the source
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

    help = "Sync Swimming data from one adapter to another."
    requires_migrations_checks = True

    def handle(
        self,
        *_args: tuple,
        **_kwargs: dict,
    ) -> None:
        """
        Handle the synchronization process between the MastodonSwimmingAdapter and DjangoSwimmingAdapter.

        This method performs the following steps:
        1. Initializes the source adapter (MastodonSwimmingAdapter).
        2. Initializes the destination adapter (DjangoSwimmingAdapter).
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
        src = MastodonSwimmingAdapter()
        dst = DjangoSwimmingAdapter()

        src.load()
        dst.load()

        src.sync_to(dst)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully synchronised.",
            ),
        )
