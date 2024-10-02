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


class MovieMetadata(BaseModel):
    title: str
    url: HttpUrl
    size: str
    hits: int
    mediainfo: HttpUrl
    ss: HttpUrl
    trailer: HttpUrl
