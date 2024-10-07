"""
This module contains exception classes 
that are used across fzmovies_api
"""


class LoadIndexError(Exception):
    """fzmovies.net failed to load successfully"""

    pass


class ZeroSearchResults(Exception):
    """Search query returned no results"""

    pass


class SessionExpired(Exception):
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


class TargetPageURLNotFound(Exception):
    """The page to navigate to has `null` as its url"""

    pass
