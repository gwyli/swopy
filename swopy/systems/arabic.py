"""Arabic numeral system - compatibility module.

The Arabic class resides in hindu_arabic.py; this module re-exports it so
that existing code referencing systems.arabic.Arabic continues to work.
"""

from .hindu_arabic import Arabic

__all__ = ["Arabic"]
