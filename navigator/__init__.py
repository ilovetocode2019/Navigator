"""
omsnav: Interface for OSM routing and handling 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A python library for handling and finding routes with OSM data with Dijkstra's algorithm.

:copyright: (c) 2023 ilovetocode
:license: MIT, see LICENSE for more details.
"""

__title__ = "navigator"
__author__ = "ilovetocode"
__license__ = "MIT"
__copyright__ = "Copyright 2023 ilovetocode"
__version__ = "0.1.0a"

from collections import namedtuple

from .core import *
from .maps import *

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=0, minor=1, micro=0, releaselevel="alpha", serial=0)
