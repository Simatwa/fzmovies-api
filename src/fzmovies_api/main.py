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
import typing as t
from tqdm import tqdm
from colorama import Fore
from os import path, getcwd
from fzmovies_api import logger


class Search(hunter.Index):
    """Perform core basics of locating the desired movie"""

    def __init__(
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

        super().__init__()
        self.query = query
        self.searchby = searchby
        self.category = category

    def __str__(self):
        f"<fzmovies_api.main.Search query='{self.query}',searchby='{self.searchby},category='{self.category}'>"

    @property
    def html_contents(self) -> str:
        """Results of the movie search"""
        return self.search(self.query, self.searchby, self.category)

    @property
    def results(self) -> models.SearchResults:
        """Modelled list of movies found"""
        return handler.search_handler(self.html_contents)


class Navigate:
    """Proceed over to target movie"""

    def __init__(self, target_movie: models.MovieInSearch):
        """Initializes `Navigate`

        Args:
            search_results (MovieInSearch): Modelled search results.
        """
        assert isinstance(target_movie, models.MovieInSearch), (
            "search_results must be an instance of "
            f"'{models.MovieInSearch}' not '{type(target_movie)}'"
        )
        self.target_movie = target_movie

    def __str__(self):
        f"<fzmovies_api.main.Navigate target_movie='{self.target_movie}'>"

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
        return f"<DownloadLinks movie_file='{self.movie_file}'>"

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

    @property
    def last_url(self) -> str:
        """Last url pointing to movie file"""
        return handler.final_download_link_handler(
            hunter.Metadata.download_link(self.download_link.url)
        )

    def save(
        self,
        filename: str,
        dir: str = getcwd(),
        progress_bar=True,
        quiet: bool = False,
        chunk_size: int = 512,
        resume: bool = False,
    ):
        """Save the movie in disk
        Args:
            filename (str): Movie filename
            dir (str, optional): Directory for saving the contents Defaults to current directory.
            progress_bar (bool, optional): Display download progress bar. Defaults to True.
            quiet (bool, optional): Not to stdout anything. Defaults to False.
            chunk_size (int, optional): Chunk_size for downloading files in KB. Defaults to 512.
            resume (bool, optional):  Resume the incomplete download. Defaults to False.

        Raises:
            FileExistsError:  Incase of `resume=True` but the download was complete
            Exception: _description_

        Returns:
            str: Path where the movie contents have been saved to.
        """
        current_downloaded_size = 0
        current_downloaded_size_in_mb = 0
        save_to = path.join(dir, filename)
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
            current_downloaded_size_in_mb = round(
                current_downloaded_size / 1000000, 2
            )  # convert to mb

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

        size_in_mb = round(size_in_bytes / 1000000, 2) + current_downloaded_size_in_mb
        chunk_size_in_bytes = chunk_size * 1024

        saving_mode = "ab" if resume else "wb"
        if progress_bar:
            if not quiet:
                print(f"{filename}")
            with tqdm(
                total=size_in_bytes + current_downloaded_size,
                bar_format="%s%d MB %s{bar} %s{l_bar}%s"
                % (Fore.GREEN, size_in_mb, Fore.CYAN, Fore.YELLOW, Fore.RESET),
                initial=current_downloaded_size,
            ) as p_bar:
                # p_bar.update(current_downloaded_size)
                with open(save_to, saving_mode) as fh:
                    for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                        fh.write(chunks)
                        p_bar.update(chunk_size_in_bytes)
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

    def __init__(self, link_index: t.Literal[0, 1] = 0, *args, **kwargs):
        """Initializes `Auto`

        Args:
            link_index (t.Literal[0,1], optional): Index of movie file link to proceed with
                0 - low quality  & small size, 1 - high quality & large size. Defaults to 0.
            The rest are arguments for initializing `Search`.

        Example:
        ```python
          from fzmovies_api import Auto
          start = Auto(query="Jason Statham", searchby="Starcast")
          start.run(filename="Fast and furious shows and hobbs.mp4")
          # or simply
          start.run()
        ```
        """

        super().__init__(*args, **kwargs)
        self.target = self.results.movies[0]
        self.link_index = link_index

    def run(self, *args, **kwargs):
        """Start auto mode.
        Args:
            Rest are arguments for `Download.save`
        """
        movie_file = Navigate(self.target).results.files[0]
        download_movie = DownloadLinks(movie_file).results
        download_link = download_movie.links[0]
        if not kwargs.get("filename"):
            kwargs["filename"] = download_movie.filename
        download = Download(download_link).save(*args, **kwargs)
