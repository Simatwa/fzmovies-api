"""
This package does the Lord's work
of automating the process of downloading a movie
using fzmovies.net. 

Right from performing `search` query down to downloading
it in your desired quality.
"""

from importlib import metadata
import logging

try:
    __version__ = metadata.version("fzmovies-api")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/fzmovie-api"

logger = logging.getLogger(__name__)
