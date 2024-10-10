"""
This module provides template
for generating essential movies' metadata
for smoother fzmovies.net interaction.

The models are not limited to:
- In search movie results
- Specific movie metadata
- Specific movie file metadata
- Recommended movies
- Download links
"""

from pydantic import BaseModel, HttpUrl
import typing as t


class MovieInSearch(BaseModel):
    """Listed results of query
    `url` : Link to the movie page
    `title` : Movie title
    `year` : Movie release year
    `distribution` : Movie distribution name.
    `about` : Movie plot
    `cover_photo` : Link to movie's release photo
    """

    url: HttpUrl
    title: str
    year: int
    distribution: str
    about: str
    cover_photo: HttpUrl

    def __str__(self):
        return f'<MovieInSearch title="{self.title}",year={self.year}>'


class SearchResults(BaseModel):
    """Joined listed results of query
    `movies` : List of `MovieInSearch`
    `first_page` : Link to the first page of the results.
    `previous_page` : Link to the previuos page of the results.
    `next_page` : Link to next page of the results.
    `last_page` : Link to the last page of the results.
    """

    movies: list[MovieInSearch]
    first_page: t.Union[HttpUrl, None] = None
    previous_page: t.Union[HttpUrl, None] = None
    next_page: t.Union[HttpUrl, None] = None
    last_page: t.Union[HttpUrl, None] = None

    def __str__(self):
        return f"<SearchResults movies=[{ ' | '.join([str(movie) for movie in self.movies]) }]>"

    def __add__(self, other: "SearchResults") -> "SearchResults":
        if not isinstance(other, SearchResults):
            raise ValueError(
                f"Operand must be an instance of {SearchResults} not {type(other)}"
            )

        return SearchResults(
            movies=self.movies + other.movies,
            first_page=other.first_page,
            previous_page=other.previous_page,
            next_page=other.next_page,
            last_page=other.last_page,
        )


class FileMetadata(BaseModel):
    """Movie file
    `title` : ..
    `url` : Link to the movie file.
    `size` : Size of the movie file.
    `hits` : File download count
    `mediainfo` : ..
    """

    title: str
    url: HttpUrl
    size: str
    hits: int
    mediainfo: HttpUrl
    ss: HttpUrl | None = None

    def __str__(self):
        return f'<FileMetadata title="{self.title}",size="{self.size}">'


class RecommendedMovie(BaseModel):
    """Movies recommended by site
    `title` : Recommed movie title
    `url` : Link to the movie page
    `cover_photo` : Link to movie's release photo.
    """

    title: str
    url: HttpUrl
    cover_photo: HttpUrl

    def __str__(self):
        return f'<RecommendedMovie title="{self.title}">'


class MovieFiles(BaseModel):
    """Collection of movie files
    `files` : List of `FileMetadata`
    `trailer` : YouTube link to movie's trailer.
    `recommended` : List of `RecommendedMovie`
    """

    files: list[FileMetadata]
    trailer: t.Union[HttpUrl, None]
    recommended: list[RecommendedMovie]

    def __str__(self):
        return f'<MovieFiles files="{" | ".join([str(file) for file in self.files])}">'


class DownloadLink(BaseModel):
    """Link to download the movie
    `url` : Download link
    `connections` : Download connections
    """

    url: HttpUrl
    connections: int

    def __str__(self):
        return f'<DownloadLink url="{self.url}", connections={self.connections}>'


class DownloadMovie(BaseModel):
    """Download metadata
    `filename` : Movie filename
    `links` : List of `DownloadLink`
    `size` : Movie file size.
    `info` : In-download page message.
    """

    filename: str
    links: list[DownloadLink]
    size: str
    info: str

    def __str__(self):
        return (
            f'<DownloadMovie filename="{self.filename}",'
            f' links={len(self.links)}, size="{self.size}">'
        )
