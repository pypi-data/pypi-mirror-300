"""
Return a simple SVG favicon.

This view handles GET requests and returns an SVG image containing a swimmer emoji.
The SVG is served with the appropriate content type for SVG images.

Args:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: An HTTP response containing the SVG favicon.
"""

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def favicon(
    _: HttpRequest,
) -> HttpResponse:
    """Return a simple SVG favicon."""
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            '<text y=".9em" font-size="90">🏊‍♀️</text>'
            "</svg>"
        ),
        content_type="image/svg+xml",
    )
