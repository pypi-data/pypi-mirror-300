"""
This module defines the version information for the HTTP package.

Attributes:
    __version__ (str): The current version of the HTTP package.
    __version_info__ (tuple): A tuple containing the major, minor, and patch version numbers.
"""

__version__ = "0.1.0"
__version_info__ = tuple(map(int, __version__.split("+")[0].split(".")))
