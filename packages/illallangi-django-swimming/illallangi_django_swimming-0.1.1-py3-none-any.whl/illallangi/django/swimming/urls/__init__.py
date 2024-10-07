"""
URL configuration for the swimming application.

This module defines the URL patterns for the swimming app, including:
- A redirect from the root URL to the "swims/" URL.
- A URL pattern for the "swims/" view.

Routes:
- "" : Redirects to "swims/".
- "swims/" : Maps to the `views.swims` view.

Imports:
- `re_path` from `django.urls` for defining URL patterns.
- `RedirectView` from `django.views.generic` for handling URL redirects.
- `views` from `illallangi.django.swimming` for the application-specific view functions.
"""

from django.urls import include, re_path

from illallangi.django.swimming import views

app_name = "swimming"

urlpatterns = [
    re_path(
        "^$",
        views.home_html,
        name="home_html",
    ),
    re_path(
        "^favicon.svg$",
        views.favicon,
        name="favicon",
    ),
    re_path(
        "^favicon.ico$",
        views.favicon,
    ),
    re_path(
        "^swims/",
        include("illallangi.django.swimming.urls.swim"),
    ),
]
