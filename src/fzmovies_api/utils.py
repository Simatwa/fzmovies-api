from bs4 import BeautifulSoup as bts
from os import path

site_url = "https://fzmovies.net/"


def souper(contents: str) -> bts:
    """Converts str object to `soup`"""
    return bts(contents, "html.parser")


def get_absolute_url(relative_url: str) -> str:
    """Makes absolute url from relative url"""
    if relative_url.startswith("/"):
        relative_url = relative_url[1:]
    return path.join(site_url, relative_url)
