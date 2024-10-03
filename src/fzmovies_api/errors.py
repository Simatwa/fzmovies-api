class LoadIndexError(Exception):
    """fzmovies.net failed to load successfully"""

    pass


class ZeroSearchResults(Exception):
    """Search query returned no results"""

    pass
