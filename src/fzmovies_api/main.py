"""
This module does the simple work
of linking the `handler` module (html)
with `hunter` (models) while providing
a higher level API.

It achieves this through 4 classes
- `Search` : Movie look-up
- `Navigate` : Progress to the targeted movie
- `DownloadLinks` : Links to the downloadable movie file
- `Download` : Download the movie file
- `Auto` : Ultimately download items of index 0.
"""

import fzmovies_api.hunter as hunter
import fzmovies_api.handlers as handler
import fzmovies_api.models as models
import fzmovies_api.utils as utils
import typing as t
from tqdm import tqdm
from os import path, getcwd
from fzmovies_api import logger
from pathlib import Path
from fzmovies_api.filters import fzmoviesFilterType, Filter, SearchNavigatorFilter


class Search(hunter.Index):
    """Perform core basics of locating the desired movie"""

    def __init__(
        self,
        query: str | fzmoviesFilterType,
        searchby: t.Literal["Name", "Director", "Starcast"] = "Name",
        category: t.Literal["All", "Bollywood", "Hollywood", "DHollywood"] = "All",
    ):
        """
        Initializes `Search`
        Args:
            query (str|fzmoviesFilterType): Search query.
            searchby (t.Literal["Name", "Director", "Starcast"], optional): Search category. Defaults to "Name".
            category (t.Literal["All", "Bollywood", "Hollywood", "DHollywood"], optional): Movie category. Defaults to "All".
        """

        super().__init__()
        self.query = query
        if isinstance(query, Filter):
            self.searchby = query.__class__.__name__
            self.category = "Unknown"
            self.is_filter = True
        else:
            self.is_filter = False
            self.searchby = searchby
            self.category = category

        self._latest_results = None

    def __str__(self):
        return f"<fzmovies_api.main.Search query='{self.query}',searchby='{self.searchby},category='{self.category}'>"

    @property
    def html_contents(self) -> str:
        """Results of the movie search"""
        return (
            self.query.get_contents()
            if self.is_filter
            else self.search(self.query, self.searchby, self.category)
        )

    @property
    def results(self) -> models.SearchResults:
        """Modelled search results"""
        resp = (
            self.query.get_results()
            if self.is_filter
            else handler.search_handler(self.html_contents)
        )
        self._latest_results = resp
        return resp

    @property
    def all_results(self) -> models.SearchResults:
        """All search results"""
        return self.get_all_results()

    def get_all_results(
        self, stream: bool = False, limit: int = 1000000
    ) -> models.SearchResults | t.Generator[models.SearchResults, None, None]:
        """Fetch all search results

        Args:
            stream (bool, optional): Yield results. Defaults to False.
            limit (int, optional): Total movies not to exceed - `multiple of 20`. Defaults to 1000000.

        Returns:
            models.SearchResults | t.Generator[models.SearchResults, None, None]
        """

        def for_stream(self, limit):
            total_movies_search = 0
            while True:
                r: models.SearchResults = self.results
                total_movies_search += len(r.movies)
                yield r
                if r.next_page:
                    self = self.next()
                else:
                    break

                if total_movies_search >= limit:
                    break

        def for_non_stream(self, limit):
            cache = None
            for results in for_stream(self, limit):
                if cache is None:
                    cache = results
                else:
                    cache = cache + results
            return cache

        return for_stream(self, limit) if stream else for_non_stream(self, limit)

    def first(self) -> "Search":
        """Navigate to the first page of search-results

        Returns:
            Search
        """
        assert self._latest_results != None, "Query results first before navigating."
        return Search(
            query=SearchNavigatorFilter(
                self._latest_results,
                "first",
            )
        )

    def previous(self) -> "Search":
        """Navigate to the previous page of search-results

        Returns:
            Search
        """
        assert self._latest_results != None, "Query results first before navigating."
        return Search(
            query=SearchNavigatorFilter(
                self._latest_results,
                "previous",
            )
        )

    def next(self) -> "Search":
        """Navigate to the next page of search-results

        Returns:
            Search
        """
        assert self._latest_results != None, "Query results first before navigating."
        return Search(
            query=SearchNavigatorFilter(
                self._latest_results,
                "next",
            )
        )

    def last(self) -> "Search":
        """Navigate to the last page of search-results

        Returns:
            Search
        """
        assert self._latest_results, "Query results first before navigating."
        return Search(
            query=SearchNavigatorFilter(
                self._latest_results,
                "last",
            )
        )


class Navigate:
    """Proceed over to the target movie"""

    def __init__(self, target_movie: models.MovieInSearch):
        """Initializes `Navigate`

        Args:
            search_results (models.MovieInSearch): Modelled search results.
        """
        assert isinstance(target_movie, models.MovieInSearch), (
            "search_results must be an instance of "
            f"'{models.MovieInSearch}' not '{type(target_movie)}'"
        )
        self.target_movie = target_movie

    def __str__(self):
        return f"<fzmovies_api.main.Navigate target_movie='{self.target_movie}'>"

    @property
    def html_contents(self) -> str:
        """Movie page"""
        return hunter.Metadata.movie_page(self.target_movie.url)

    @property
    def results(self) -> models.MovieFiles:
        """Movie files"""
        return handler.movie_handler(self.html_contents)


class DownloadLinks:
    """Get links to downloadable movie file"""

    def __init__(self, movie_file: models.FileMetadata):
        """Initializes `Download`

        Args:
            movie_file (models.FileMetadata): Targeted movie file
        """
        assert isinstance(movie_file, models.FileMetadata), (
            "movie_file must be an instance of "
            f"'{models.FileMetadata}' not '{type(movie_file)}'"
        )
        self.movie_file = movie_file

    def __str__(self):
        return f"<fzmovies_api.main.DownloadLinks movie_file='{self.movie_file}'>"

    @property
    def html_contents(self):
        """Html contents of to-download page"""
        return hunter.Metadata.to_download_page(self.movie_file.url)

    @property
    def results(self) -> models.DownloadMovie:
        """Links to downloadable movie file"""
        download_url = handler.to_download_handler(self.html_contents)
        links_page = hunter.Metadata.to_download_links_page(download_url)

        return handler.download_links_handler(links_page)


class Download:
    """Download the movie file"""

    def __init__(self, download_link: models.DownloadLink):
        """Initializes `Download`

        Args:
            download_link (models.DownloadLink): Url for the movie file
        """
        assert isinstance(download_link, models.DownloadLink), (
            "movie_file must be an instance of "
            f"'{models.DownloadLink}' not '{type(download_link)}'"
        )
        self.download_link = download_link

    def __str__(self):
        return f"<fzmovies_api.main.Download : {self.download_link}>"

    @property
    def last_url(self) -> str:
        """Last url pointing to movie file"""
        return handler.final_download_link_handler(
            hunter.Metadata.download_link(self.download_link.url.__str__())
        )

    def save(
        self,
        filename: str,
        dir: str = getcwd(),
        progress_bar=True,
        quiet: bool = False,
        chunk_size: int = 512,
        resume: bool = False,
        leave: bool = True,
        colour: str = "cyan",
        simple: bool = True,
    ):
        """Save the movie in disk
        Args:
            filename (str): Movie filename
            dir (str, optional): Directory for saving the contents Defaults to current directory.
            progress_bar (bool, optional): Display download progress bar. Defaults to True.
            quiet (bool, optional): Not to stdout anything. Defaults to False.
            chunk_size (int, optional): Chunk_size for downloading files in KB. Defaults to 512.
            resume (bool, optional):  Resume the incomplete download. Defaults to False.
            leave (bool, optional): Keep all traces of the progressbar. Defaults to True.
            colour (str, optional): Progress bar display color. Defaults to "cyan".
            simple (bool, optional): Show percentage and bar only in progressbar. Deafults to False.

        Raises:
            FileExistsError:  Incase of `resume=True` but the download was complete
            Exception: _description_

        Returns:
            str: Path where the movie contents have been saved to.
        """
        current_downloaded_size = 0
        current_downloaded_size_in_mb = 0
        save_to = Path(dir) / filename
        movie_file_url = self.last_url

        def pop_range_in_session_headers():
            if hunter.session.headers.get("Range"):
                hunter.session.headers.pop("Range")

        if resume:
            assert path.exists(save_to), f"File not found in path - '{save_to}'"
            current_downloaded_size = path.getsize(save_to)
            # Set the headers to resume download from the last byte
            hunter.session.headers.update(
                {"Range": f"bytes={current_downloaded_size}-"}
            )
            current_downloaded_size_in_mb = current_downloaded_size / 1000000

        default_content_length = 0

        resp = hunter.session.get(movie_file_url, stream=True)

        size_in_bytes = int(resp.headers.get("content-length", default_content_length))
        if not size_in_bytes:
            if resume:
                raise FileExistsError(
                    f"Download completed for the file in path - '{save_to}'"
                )
            else:
                raise Exception(
                    f"Cannot download file of content-length {size_in_bytes} bytes"
                )

        if resume:
            assert (
                size_in_bytes != current_downloaded_size
            ), f"Download completed for the file in path - '{save_to}'"

        size_in_mb = (size_in_bytes / 1_000_000) + current_downloaded_size_in_mb
        chunk_size_in_bytes = chunk_size * 1_000

        saving_mode = "ab" if resume else "wb"
        if progress_bar:
            if not quiet:
                print(f"{filename}")
            with tqdm(
                desc="Downloading",
                total=round(size_in_mb, 1),
                bar_format=(
                    "{l_bar}{bar} | %(size)s MB" % (dict(size=round(size_in_mb, 1)))
                    if simple
                    else "{l_bar}{bar}{r_bar}"
                ),
                initial=current_downloaded_size_in_mb,
                unit="Mb",
                colour=colour,
                leave=leave,
            ) as p_bar:
                # p_bar.update(current_downloaded_size)
                with open(save_to, saving_mode) as fh:
                    for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                        fh.write(chunks)
                        p_bar.update(round(chunk_size_in_bytes / 1_000_000, 1))
                pop_range_in_session_headers()
                return save_to
        else:
            with open(save_to, saving_mode) as fh:
                for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                    fh.write(chunks)

            logger.info(f"{filename} - {size_in_mb}MB ✅")
            pop_range_in_session_headers()
            return save_to


class Auto(Search):
    """Performs a search and proceeds with  every first item
    all the way to downloading."""

    def __init__(self, quality: t.Literal["480p", "720p"] = "720p", *args, **kwargs):
        """Initializes `Auto`

        Args:
            quality (t.Literal[480p, 720p], optional): Video quality. Default to 720p.
            The rest are arguments for initializing `Search`.

        Example:
        ```python
          from fzmovies_api import Auto
          start = Auto(query="Jason Statham", searchby="Starcast")
          start.run(filename="Fast and furious shows and hobbs.mp4")
          # or simply
          start.run()
          # to resume incomplete downloads
          start.run(resume=True)
        ```
        """

        assert quality in utils.file_index_quality_map, (
            f"Movie quality '{quality}' is not one of"
            f" {list(utils.file_index_quality_map.keys())}"
        )
        super().__init__(*args, **kwargs)
        self.target = self.results.movies[0]
        self._movie_file_index = utils.file_index_quality_map.get(quality)

    def __str__(self):
        return f"<fzmovies_api.main.Auto : {self.target}>"

    def run(self, *args, **kwargs) -> Path:
        """Start auto mode.
        Args:
            The rest are arguments for `Download.save`

        Returns:
            Path: Absolute path to the downloaded movie file
        """
        movie_file = Navigate(self.target).results.files[self._movie_file_index]
        download_movie = DownloadLinks(movie_file).results
        download_link = download_movie.links[0]
        if not kwargs.get("filename"):
            kwargs["filename"] = download_movie.filename
        return Download(download_link).save(*args, **kwargs)


class Support:
    """Provides general helpful resources such as
    movie release qualities and FAQs.
    """

    @staticmethod
    def get_movie_release_formats() -> dict[str, str]:
        """Movie release quality and their descriptions

        Returns:
            dict[str, str]: format, description
        """
        return handler.questions_and_answers_handler(
            hunter.Metadata.questions_and_answers_content("formats")
        )

    @staticmethod
    def get_frequently_asked_questions() -> dict[str, str]:
        """Questions and answers mostly asked

        Returns:
            dict[str, str]: questions, answers
        """
        return handler.questions_and_answers_handler(
            hunter.Metadata.questions_and_answers_content("faq")
        )
