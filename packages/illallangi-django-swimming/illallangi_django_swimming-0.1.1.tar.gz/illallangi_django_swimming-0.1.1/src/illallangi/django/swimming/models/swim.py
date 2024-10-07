"""Swim represents a swimming activity with details such as URL, date, distance and laps."""

from django.db import models
from django.urls import reverse
from django_sqids import SqidsField


class Swim(
    models.Model,
):
    """
    Swim represents a swimming activity with specific details such as URL, date, distance and laps.

    Attributes:
        id (AutoField): The primary key for the model.
        url (URLField): A URL related to the swimming activity.
        date (DateField): The date of the swimming activity.
        distance (PositiveIntegerField): The distance swum in meters.
        laps (FloatField): The number of laps swum.
    Methods:
        __str__(): Returns a string representation of the Swim instance in the format "Swim {id}".
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

    date = models.DateField(
        null=False,
        blank=False,
    )

    distance = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    laps = models.FloatField(
        null=False,
        blank=False,
    )

    # Methods

    def __str__(
        self,
    ) -> str:
        """
        Return a string representation of the Swim instance.

        Returns:
            str: A string in the format "{distance}m Swim" where {distance} is the distance swam.
        """
        return f"{self.distance}m Swim"

    def get_absolute_url(
        self,
    ) -> str:
        """
        Return the absolute URL of the Swim instance.

        Returns:
            str: The absolute URL of the Swim instance.
        """
        return reverse(
            "swimming:swim_html",
            kwargs={
                "swim_slug": self.sqid,
                "swim_year": str(self.date.year).zfill(4),
                "swim_month": str(self.date.month).zfill(2),
                "swim_day": str(self.date.day).zfill(2),
            },
        )
