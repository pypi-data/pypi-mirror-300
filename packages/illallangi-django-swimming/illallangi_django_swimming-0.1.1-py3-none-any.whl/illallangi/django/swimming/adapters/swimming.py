"""SwimmingAdapter is a custom adapter for syncing swimming data using the diffsync library."""

from typing import ClassVar

import diffsync

from illallangi.django.swimming.diffsyncmodels import Swim
from illallangi.django.swimming.models import Swim as DjangoSwim


class SwimmingAdapter(diffsync.Adapter):
    """
    SwimmingAdapter is an adapter for syncing Swim objects from a Django model.

    Attributes:
        Swim (class): The Swim class to be used for creating Swim objects.
        top_level (list): A list containing the top-level object types.
        type (str): The type identifier for this adapter.
    Methods:
        load():
            Loads Swim objects from the Django model and adds them to the adapter.
    """

    Swim = Swim

    top_level: ClassVar = [
        "Swim",
    ]

    type = "django_swimming"

    def load(
        self,
    ) -> None:
        """
        Load all Swim objects from the database and adds them to the current instance.

        This method retrieves all instances of the DjangoSwim from the database,
        converts them into Swim objects, and adds them to the current instance.
        Returns:
            None
        """
        for obj in DjangoSwim.objects.all():
            self.add(
                Swim(
                    pk=obj.pk,
                    url=obj.url,
                    date=obj.date,
                    distance=obj.distance,
                    laps=obj.laps,
                ),
            )
