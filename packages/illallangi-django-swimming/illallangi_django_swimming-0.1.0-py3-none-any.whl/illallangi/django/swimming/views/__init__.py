"""
This module initializes the views for the Django swimming application.

It imports the `swims_html` view from the `swim` module and includes it in the
`__all__` list to specify the public interface of this module.

Modules:
    swim (illallangi.django.swimming.views.swim): Contains the `swims_html` view.

Attributes:
    __all__ (list): List of public objects of this module, which includes `swims_html`.
"""

from illallangi.django.swimming.views.home import home_html
from illallangi.django.swimming.views.swim import swim_html, swims_html

from .favicon import favicon

__all__ = [
    "favicon",
    "home_html",
    "swim_html",
    "swims_html",
]
