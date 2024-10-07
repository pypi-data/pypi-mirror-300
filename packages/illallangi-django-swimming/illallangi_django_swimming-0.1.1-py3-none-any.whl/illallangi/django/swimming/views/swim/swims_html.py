"""
Render the swims HTML page with pagination and breadcrumbs.

This view handles GET requests and renders the swims HTML page. It includes
pagination for the list of swims, breadcrumbs for navigation, and alternate
links for different content types.

Args:
    request (HttpRequest): The HTTP request object.
Returns:
    HttpResponse: The rendered HTML response.
"""

import calendar

from django.contrib.humanize.templatetags.humanize import ordinal
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from illallangi.django.swimming.models import Swim


@require_GET
def swims_html(
    request: HttpRequest,
    swim_year: str | None = None,
    swim_month: str | None = None,
    swim_day: str | None = None,
    **_: dict,
) -> render:
    """
    Render the swims HTML page with a list of swim objects and related metadata.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        render: The rendered HTML page for swims.
    """
    objects = Swim.objects.all()
    if swim_year:
        objects = objects.filter(date__year=swim_year)
    if swim_month:
        objects = objects.filter(date__month=swim_month)
    if swim_day:
        objects = objects.filter(date__day=swim_day)

    if objects.count() == 1:
        return redirect(
            objects.first().get_absolute_url(),
        )

    return render(
        request,
        "swimming/swims.html",
        {
            "base_template": ("partial.html" if request.htmx else "base.html"),
            "page": Paginator(
                object_list=objects.order_by("date"),
                per_page=10,
            ).get_page(
                request.GET.get("page", 1),
            ),
            "breadcrumbs": list(
                filter(
                    lambda x: x is not None,
                    [
                        {
                            "title": "Swimming",
                            "url": reverse(
                                "swimming:home_html",
                            ),
                        },
                        {
                            "title": "Swims",
                            "url": reverse(
                                "swimming:swims_html",
                            ),
                        },
                        {
                            "title": swim_year,
                            "url": reverse(
                                "swimming:swims_year",
                                kwargs={
                                    "swim_year": swim_year,
                                },
                            ),
                        }
                        if swim_year
                        else None,
                        {
                            "title": calendar.month_name[int(swim_month)],
                            "url": reverse(
                                "swimming:swims_month",
                                kwargs={
                                    "swim_year": swim_year,
                                    "swim_month": swim_month,
                                },
                            ),
                        }
                        if swim_month
                        else None,
                        {
                            "title": ordinal(swim_day),
                            "url": reverse(
                                "swimming:swims_day",
                                kwargs={
                                    "swim_year": swim_year,
                                    "swim_month": swim_month,
                                    "swim_day": swim_day,
                                },
                            ),
                        }
                        if swim_day
                        else None,
                    ],
                )
            ),
            "links": [
                {
                    "rel": "alternate",
                    "type": "text/html",
                    "href": request.build_absolute_uri(
                        reverse(
                            "swimming:swims_html",
                        ),
                    ),
                },
            ],
        },
    )
