from pydantic import BaseModel, HttpUrl
import typing as t


class MovieInSearch(BaseModel):
    url: HttpUrl
    title: str
    year: int
    distribution: str
    about: str
    cover_photo: HttpUrl


class SearchResults(BaseModel):
    movies: list[MovieInSearch]
    next_page: t.Union[HttpUrl, None] = None
    last_page: t.Union[HttpUrl, None] = None


class FileMetadata(BaseModel):
    title: str
    url: HttpUrl
    size: str
    hits: int
    mediainfo: HttpUrl
    ss: HttpUrl


class RecommendedMovies(BaseModel):
    title: str
    url: HttpUrl
    cover_photo: HttpUrl


class MovieFiles(BaseModel):
    files: list[FileMetadata]
    trailer: HttpUrl
    recommended: list[RecommendedMovies]
