"""
This module initializes the swim views for the Django swimming application.

It imports the `swims_html` view from the `swims_html` module and includes it in the `__all__` list for public API exposure.

Modules:
    swims_html: A view that handles the HTML representation of swims.

Attributes:
    __all__ (list): A list of public objects of this module, as interpreted by `import *`.
"""

from .swim_html import swim_html
from .swims_html import swims_html

__all__ = [
    "swim_html",
    "swims_html",
]
