"""
- Load index page
- Perform search
- Select the target movie
- Proceed to download page
- Select link
"""

import re
import requests
import typing as t
from fzmovies_api import errors, logger
import fzmovies_api.models as models

session = requests.Session()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "referer": "https://fzmovies.net/",
}

session.headers.update(headers)

request_timeout = 20


class Index:
    """
    Load index page & perform search
    """

    url = "https://fzmovies.net"
    search_url = "https://fzmovies.net/csearch.php"
    searchby_options = ["Name", "Director", "Starcast"]
    category_options = ["All", "Bollywood", "Hollywood", "DHollywood"]
    session_is_initialized = False

    def __init__(
        self,
    ):
        """Instantiates Index"""
        if not self.session_is_initialized:
            load_index_resp = session.get(self.url, timeout=request_timeout)
            if not load_index_resp.ok:
                logger.debug(
                    f"Headers - {load_index_resp.headers} \nResponse - {load_index_resp.text}"
                )
                raise errors.LoadIndexError(
                    f"Failed to load index page - ({load_index_resp.status_code} : {load_index_resp.reason})"
                )
            self.index_resp = load_index_resp

    def __str__(self):
        return f"<fzmoviesIndex_{self.index_resp.reason}>"

    def search(
        self,
        query: str,
        searchby: t.Literal["Name", "Director", "Starcast"] = "Name",
        category: t.Literal["All", "Bollywood", "Hollywood", "DHollywood"] = "All",
    ):
        """
        Args:
            query (str): Search query.
            searchby (t.Literal["Name", "Director", "Starcast"], optional): Search category. Defaults to "Name".
            category (t.Literal["All", "Bollywood", "Hollywood", "DHollywood"], optional): Movie category. Defaults to "All".
        """
        assert type(query) is str, f"Query must of {str} datatype only"
        assert (
            searchby in self.searchby_options
        ), f"Searchby '{searchby}' is NOT one of '{self.searchby_options}'"
        assert (
            category in self.category_options
        ), f"Category '{category}' is NOT one of '{self.category_options}'"

        payload = dict(
            searchname=query,
            Search="Search",
            searchby=searchby,
            category=category,
            vsearch="",
        )
        resp = session.post(self.search_url, data=payload, timeout=request_timeout)
        resp.raise_for_status()
        return resp.text


class Metadata:
    """Fetch html contents for :
    - Movie page
    - To download page
    - To download links page
    """

    def __init__(self):
        pass

    def _get_resource(self, url: str, timeout: int = 20, *args, **kwargs):
        """Fetch online resource

        Args:
            timeout (int): Http request timeout
            url (str): Url to resource
        """
        resp = session.get(url, timeout=timeout, *args, **kwargs)
        resp.raise_for_status()
        return resp

    def movie_page(self, movie_url: str) -> str:
        """Requests movie page

        Args:
            movie_url (str): Link to movie page

        Returns:
            str: Html contents for the page.
        """
        movie_url = str(movie_url)
        assert movie_url.endswith(".htm"), f"Invalid movie page url '{movie_url}'"
        return self._get_resource(movie_url).text

    def to_download_page(self, movie_file_url: str) -> str:
        """Requests page leading to download links

        Args:
            movie_file_url (str):  Link to movie file

        Returns:
            str: Html contents of the to-download page.
        """
        movie_file_url = str(movie_file_url)
        assert (
            "/download1.php?downloadoptionskey=" in movie_file_url
        ), f"Invalid movie-file url - '{movie_file_url}'"
        return self._get_resource(movie_file_url).text

    def to_download_links_page(self, download_url: str) -> str:
        """Requests page containing download links

        Args:
            download_url (str): The link to the page containing links

        Returns:
            str: Html content of the page.
        """
        download_url = str(download_url)
        assert (
            "/download.php?downloadkey=" in download_url
        ), f"Invalid to-download links url - '{download_url}'"
        return self._get_resource(download_url).text
