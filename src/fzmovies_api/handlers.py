"""
Extracts key data from raw html contents 
and use them to generate models
"""

import re
import fzmovies_api.models as models
import fzmovies_api.utils as utils


def search_handler(contents: str) -> models.SearchResults:
    """Make model from search results (html)

    Args:
        contents (str): Html fomatted data

    Returns:
        SearchResults: Modelled search results
    """
    soup = utils.souper(contents)

    search_result_items: list[dict[str, str]] = []

    for search_result in soup.find_all("div", {"class": "mainbox"}):
        url = search_result.find("a").get("href")
        title_soup, year_soup, distribution_soup, about_soup = search_result.find(
            "span"
        ).find_all("small")
        title = title_soup.text.strip()
        year = re.sub(r"\(|\)", "", year_soup.text.strip())
        distribution = re.sub(r"\(|\)", "", distribution_soup.text.strip())
        about = about_soup.text.strip()
        cover_photo = search_result.find("img").get("src")
        search_result_items.append(
            dict(
                url=utils.get_absolute_url(url),
                title=title,
                year=year,
                distribution=distribution,
                about=about,
                cover_photo=utils.get_absolute_url(cover_photo),
            )
        )

    pages = soup.find("div", {"class": "mainbox2"})
    if pages:
        next_page_soup, last_page_soup = pages.find_all("a")
        next_page = next_page_soup.get("href")
        last_page = last_page_soup.get("href")
    else:
        next_page = last_page = None

    return models.SearchResults(
        movies=search_result_items, next_page=next_page, last_page=last_page
    )


def movie_handler(contents: str) -> models.MovieFiles:
    """Make model from movie metadata (html)"""
    movie_files: list[dict[str, str]] = []
    recommended_movies: list[dict[str, str]] = []
    soup = utils.souper(contents)
    trailer = soup.find(
        "iframe",
        {
            "allow": "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        },
    ).get("src")

    for movie in soup.find("div", {"class": "owl-carousel owl-theme"}).find_all("a"):
        title = movie.get("alt")
        url = movie.get("href")
        cover_photo = movie.find("img").get("src")
        recommended_movies.append(
            dict(
                title=title,
                url=utils.get_absolute_url(url),
                cover_photo=utils.get_absolute_url(cover_photo),
            )
        )

    for movie_file in soup.find_all("ul", {"class": "moviesfiles"}):
        urls = movie_file.find_all("a")
        title_url = urls[0]
        title = title_url.text.strip()
        url = title_url.get("href")
        dcounter = re.sub(
            r"\(|\)|\{|\}", "", movie_file.find("dcounter").text.strip()
        ).split(" ")
        size = " ".join(dcounter[:2])
        hits = dcounter[-3]
        mediainfo = urls[1].get("href")
        ss = urls[2].get("href")
        movie_files.append(
            dict(
                title=title,
                url=utils.get_absolute_url(url),
                size=size,
                hits=hits,
                mediainfo=utils.get_absolute_url(mediainfo),
                ss=utils.get_absolute_url(ss),
            )
        )
    return models.MovieFiles(
        files=movie_files, trailer=trailer, recommended=recommended_movies
    )
