"""
This module initializes the admin interface for the swimming application.

It imports the SwimModelAdmin class from the swim module and includes it in the
__all__ list to specify the public API of this module.

Classes:
    SwimModelAdmin: Admin interface for the Swim model.
"""

from .swim import SwimModelAdmin

__all__ = [
    "SwimModelAdmin",
]
