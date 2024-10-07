"""
Swim represents a swimming activity with details such as date, laps, distance, and URL.

Attributes:
    pk: The primary key for the model.
    url: A URL related to the swimming activity.
    date: The date of the swimming activity.
    distance: The distance swum in meters.
    laps: The number of laps swum.

Methods:
    __str__(): Returns a string representation of the Swim instance in the format "Swim {id}".
"""

import diffsync

from illallangi.django.swimming.models.swim import Swim as ModelSwim


class Swim(
    diffsync.DiffSyncModel,
):
    """
    Swim represents a swimming activity with specific details such as date, laps, distance, and URL.

    Attributes:
        pk: The primary key for the model.
        url: A URL related to the swimming activity.
        date: The date of the swimming activity.
        distance: The distance swum in meters.
        laps: The number of laps swum.
    Methods:
        __str__(): Returns a string representation of the Swim instance in the format "Swim {id}".
    """

    pk: int
    url: str
    date: str
    distance: int
    laps: float

    _modelname = "Swim"
    _identifiers = ("url",)
    _attributes = (
        "date",
        "distance",
        "laps",
    )

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Swim":
        """
        Create a Swim instance.

        This method updates or creates a Swim object using the provided ids and attrs,
        then creates a Swim instance with the updated or created Swim object's
        primary key and the provided ids and attrs.
        Args:
            cls: The class that this method is called on.
            adapter: The adapter to use for creating the Swim instance.
            ids (dict): A dictionary containing the identifiers for the Swim object.
            attrs (dict): A dictionary containing the attributes for the Swim object.
        Returns:
            Swim: The created Swim instance.
        """
        obj = ModelSwim.objects.update_or_create(
            url=ids["url"],
            defaults={
                "date": attrs["date"],
                "distance": attrs["distance"],
                "laps": attrs["laps"],
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
    ) -> "Swim":
        """
        Update the current Swim instance with the provided attributes.

        Args:
            attrs (dict): A dictionary of attributes to update the instance with.
        Returns:
            Swim: The updated Swim instance.
        """
        ModelSwim.objects.filter(
            pk=self.pk,
        ).update(
            **attrs,
        )

        return super().update(attrs)

    def delete(
        self,
    ) -> "Swim":
        """
        Delete the current Swim instance from the database.

        This method first deletes the associated Swim object using its primary key (pk),
        and then calls the superclass's delete method to remove the Swim instance.
        Returns:
            Swim: The deleted Swim instance.
        """
        ModelSwim.objects.get(
            pk=self.pk,
        ).delete()

        return super().delete()
