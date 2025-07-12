"""
This module does the ground-work of interacting
with fzmovies.net in fetching the required resources 
that revolves around:
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
import fzmovies_api.utils as utils

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

    url = utils.site_url
    search_url = utils.get_absolute_url("/csearch.php")
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
        Performs `POST` request search
        Args:
            query (str): Search query.
            searchby (t.Literal["Name", "Director", "Starcast"], optional): Search category. Defaults to "Name".
            category (t.Literal["All", "Bollywood", "Hollywood", "DHollywood"], optional): Movie category. Defaults to "All".
        """
        assert (
            type(query) is str
        ), f"Query must be of {str} datatype only not {type(query)}"
        if not query:
            raise ValueError("Query cannot be empty")
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
    - To-download page
    - To-download-links page
    - Movies m
    """

    session_expired_pattern = r".*Your download keys have expired.*"

    question_and_answers_url_map = {
        "formats": utils.get_absolute_url("/mquality.php"),
        "faq": utils.get_absolute_url("/support.php"),
    }

    @classmethod
    def get_resource(cls, url: str, timeout: int = 20, *args, **kwargs):
        """Fetch online resource

        Args:
            timeout (int): Http request timeout
            url (str): Url to resource
        """
        if not session.cookies.get("PHPSESSID"):
            logger.debug("Initializing session")
            Index()
        resp = session.get(url, timeout=timeout, *args, **kwargs)
        resp.raise_for_status()
        if "text/html" in resp.headers.get("Content-Type", ""):
            has_expired = re.search(cls.session_expired_pattern, resp.text)
            if has_expired:
                raise errors.SessionExpired(
                    utils.get_absolute_url(
                        utils.souper(has_expired.group()).find("a").get("href")
                    ),
                )

        return resp

    @classmethod
    def movie_page(cls, movie_url: str) -> str:
        """Requests movie page

        Args:
            movie_url (str): Link to movie page

        Returns:
            str: Html contents for the page.
        """
        movie_url = str(movie_url)
        assert movie_url.endswith(".htm"), f"Invalid movie page url '{movie_url}'"
        return cls.get_resource(movie_url).text

    @classmethod
    def to_download_page(cls, movie_file_url: str) -> str:
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
        return cls.get_resource(movie_file_url).text

    @classmethod
    def to_download_links_page(cls, download_url: str) -> str:
        """Requests page containing download links

        Args:
            download_url (str): The link to the page containing links

        Returns:
            str: Html content of the page.
        """
        download_url = str(download_url)
        assert (
            "/download.php?downloadkey=" in download_url
        ), f"Invalid to-download-links url - '{download_url}'"
        return cls.get_resource(download_url).text

    @classmethod
    def download_link(cls, last_download_url: str) -> str:
        """Requests page containing final download link

        Args:
            last_download_url (str): Link to the last page

        Returns:
            str: Url pointing to the movie file ready to be downloaded.
        """
        assert (
            "/dlink.php?id=" in last_download_url
        ), f"Invalid last-download url - '{last_download_url}'"
        return cls.get_resource(last_download_url).text

    @classmethod
    def questions_and_answers_content(
        cls, category: t.Literal["formats", "faq"]
    ) -> str:
        """Requests page containing the resource.

        Args:
            category (t.Literal["formats", "faq"]): QA resource category

        Returns:
            str: HTMl contents of the page.
        """
        utils.assert_membership(category, list(cls.question_and_answers_url_map.keys()))
        return cls.get_resource(cls.question_and_answers_url_map[category]).text
