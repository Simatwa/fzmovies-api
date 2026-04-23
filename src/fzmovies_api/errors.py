"""
This module contains exception classes 
that are used across fzmovies_api
"""

class FzmoviesAPIException(Exception):
    """Base class for package exceptions"""

class LoadIndexError(FzmoviesAPIException):
    """fzmovies.net failed to load successfully"""


class ZeroSearchResults(FzmoviesAPIException):
    """Search query returned no results"""


class SessionExpired(FzmoviesAPIException):
    """Session expired and perhaps previous request was never
    made using startup session at <fzmovies_api.hunter.Index>
    """

    def __init__(self, redirect_to: str, message: str | None = None):
        """Initializer

        Args:
            redirect_to (str): Link to refer to.
            message (str | None, optional): Exception message. Defaults to None.
        """
        super().__init__(message if message else self.__class__.__doc__)
        self.redirect_to = redirect_to


class TargetPageURLNotFound(FzmoviesAPIException):
    """The page to navigate to has `null` as its url"""


class DownloadError(FzmoviesAPIException):
    """failed to download file for some reasons"""