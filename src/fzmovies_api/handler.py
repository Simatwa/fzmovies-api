"""
Bridges models and raw search
"""

import re
import fzmovies_api.models as models
import fzmovies_api.utils as utils


def search_handler(contents: str) -> models.SearchResults:
    """Template for movies search results

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
