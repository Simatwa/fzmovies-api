"""
Extracts key data from raw html contents 
and use them to generate models
"""

import re
import fzmovies_api.models as models
import fzmovies_api.utils as utils
import fzmovies_api.errors as errors


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
        span = search_result.find("span")
        if not span:
            title = soup.find("title").text.strip().split("-", 1)[1]
            raise errors.ZeroSearchResults(
                title
                + " yielded no results. Check the spelling or try broadening your search."
            )
        extract = span.find_all("small")
        if len(extract) == 4:
            title_soup, year_soup, distribution_soup, about_soup = extract
        else:
            title_soup, year_soup, about_soup = extract
            distribution_soup = utils.souper("<h4>Unknown</h4>")
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
    first_page = previous_page = next_page = last_page = last_page = None
    if pages:
        for nav in pages.find_all("a"):
            link = nav.get("href")
            text = nav.text.strip()
            if text == "First":
                first_page = link
            elif text == "Prev":
                previous_page = link
            elif text == "Next":
                next_page = link
            elif text == "Last":
                last_page = link

    return models.SearchResults(
        movies=search_result_items,
        next_page=next_page,
        last_page=last_page,
        first_page=first_page,
        previous_page=previous_page,
    )


def movie_handler(contents: str) -> models.MovieFiles:
    """Make model from movie metadata (html)"""
    movie_files: list[dict[str, str]] = []
    recommended_movies: list[dict[str, str]] = []
    soup = utils.souper(contents)
    trailer_soup = soup.find(
        "iframe",
        {
            "allow": "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        },
    )

    trailer = trailer_soup.get("src") if trailer_soup else None

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
        if not urls:
            continue
        title_url = urls[0]
        title = title_url.text.strip()
        url = title_url.get("href")
        dcounter = re.sub(
            r"\(|\)|\{|\}", "", movie_file.find("dcounter").text.strip()
        ).split(" ")
        size = " ".join(dcounter[:2])
        hits = dcounter[-3]
        mediainfo = urls[1].get("href")
        if len(urls) >= 3:
            ss = urls[2].get("href")
        else:
            ss = None
        movie_files.append(
            dict(
                title=title,
                url=utils.get_absolute_url(url),
                size=size,
                hits=hits,
                mediainfo=utils.get_absolute_url(mediainfo),
                ss=utils.get_absolute_url(ss) if ss else None,
            )
        )
    return models.MovieFiles(
        files=movie_files, trailer=trailer, recommended=recommended_movies
    )


def to_download_handler(contents: str) -> str:
    """Extract to-download-links url from to-download page

    Args:
        contents (str): to-download page contents

    Returns:
        str: to-download-links url
    """
    soup = utils.souper(contents)
    link = soup.find("a", {"id": "downloadlink"}).get("href")
    return utils.get_absolute_url(link)


def download_links_handler(contents: str) -> models.DownloadMovie:
    """Extract download links from download page and generate
    download model

    Args:
        contents (str): Html contents containing download links

    Returns:
        models.DownloadMovie: Models for download links
    """
    soup = utils.souper(contents)
    info = soup.find("div", {"class": "mainbox4"}).text.strip()
    movie_desc = soup.find("div", {"class": "moviedesc"})
    filename = movie_desc.find("textcolor1").text.strip()
    size = movie_desc.find("textcolor2").text.strip()

    download_link_items: list[dict] = []

    for dlink in soup.find_all("ul", {"class": "downloadlinks"}, limit=3)[-1].find_all(
        "li"
    ):
        url = dlink.find("a").get("href")
        connections = re.sub(r"\(|\)", "", dlink.find("dcounter").text.strip()).split(
            " "
        )[0]
        download_link_items.append(
            dict(url=utils.get_absolute_url(url), connections=connections)
        )
    return models.DownloadMovie(
        filename=filename, links=download_link_items, size=size, info=info
    )


def final_download_link_handler(contents: str) -> str:
    """Extracts the last url pointing to the movie file"""

    soup = utils.souper(contents)

    return soup.find("div", {"class": "mainbox3"}).find("a").get("href")


def questions_and_answers_handler(contents: str) -> dict[str, str]:
    """Extracts question and answers from html contents to
    form dictionary.

    Returns:
        dict[str, str]: Question and their corresponding answers.
    """
    soup = utils.souper(contents)
    formats_soup = soup.find_all("div", {"class": "question"})
    descriptions_soup = soup.find_all("div", {"class": "answer"})
    formats_list: list[str] = [
        " ".join(format.text.strip().split(" ")[1:]) for format in formats_soup
    ]
    descriptions_list: list[str] = [
        description.text.strip() for description in descriptions_soup
    ]
    return dict(zip(formats_list, descriptions_list))
