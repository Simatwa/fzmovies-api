"""
This package does the Lord's work
of automating the process of downloading a movie
from fzmovies.live

Right from performing `search` query down to downloading
it in your desired quality.
"""

import logging
from importlib import metadata

try:
    __version__ = metadata.version("fzmovies-api")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/fzmovie-api"

logger = logging.getLogger(__name__)

from fzmovies_api.main import Auto, Download, DownloadLinks, Navigate, Search, Support

__all__ = ["Auto", "Download", "DownloadLinks", "Navigate", "Search", "Support"]
