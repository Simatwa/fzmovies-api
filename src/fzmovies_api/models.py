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


class SearchResults(BaseModel):
    """Joined listed results of query
    `movies` : List of `MovieInSearch`
    `next_page` : Link to next page of the results.
    `last_page` : Link to the last page of the results.
    """

    movies: list[MovieInSearch]
    next_page: t.Union[HttpUrl, None] = None
    last_page: t.Union[HttpUrl, None] = None


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
    ss: HttpUrl


class RecommendedMovie(BaseModel):
    """Movies recommended by site
    `title` : Recommed movie title
    `url` : Link to the movie page
    `cover_photo` : Link to movie's release photo.
    """

    title: str
    url: HttpUrl
    cover_photo: HttpUrl


class MovieFiles(BaseModel):
    """Collection of movie files
    `files` : List of `FileMetadata`
    `trailer` : YouTube link to movie's trailer.
    `recommended` : List of `RecommendedMovie`
    """

    files: list[FileMetadata]
    trailer: HttpUrl
    recommended: list[RecommendedMovie]


class DownloadLink(BaseModel):
    """Link to download the movie
    `url` : Download link
    `connections` : Download connections
    """

    url: HttpUrl
    connections: int


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
