"""
This module contains search filters
along with page navigation filters
"""

from abc import ABC, abstractmethod
from fzmovies_api.hunter import Metadata
import fzmovies_api.models as models
import fzmovies_api.errors as errors
from fzmovies_api.handlers import search_handler
from fzmovies_api.utils import category_id_map, assert_membership, get_absolute_url
from datetime import datetime
import typing as t


class Filter(ABC):
    """Abstract Base class for filters"""

    url: str = None
    """Absolute url to the fzmovies-page containing the movie listings"""

    @abstractmethod
    def get_contents(self) -> str:
        """Get Html contents of the url

        Returns:
            str: html contents
        """
        raise NotImplementedError("This method needs to be implemented in subclass.")

    @abstractmethod
    def get_results(self) -> models.SearchResults:
        """Get modelled version of the results

        Returns:
            models.SearchResults: Results
        """
        raise NotImplementedError("This method needs to be implemented in subclass.")


class FilterBase(Filter):
    """Parent base class for Filter classes"""

    init_with_category: bool = True
    """Accepts category argument while initializing"""

    init_with_arg: bool = True
    """Accept special argument other than category"""

    def get_contents(self) -> str:
        """Fetch Html contents of the url

        Returns:
            str: html contents
        """
        return Metadata.get_resource(self.url).text

    def get_results(self) -> models.SearchResults:
        """Get modelled version of the movie list

        Returns:
            models.SearchResults: Results
        """
        return search_handler(self.get_contents())


class IMDBTop250Filter(FilterBase):
    """IMDB TOp 250 movies filter"""

    init_with_arg = False
    init_with_category = False

    url = get_absolute_url("/imdb250.php")


class OscarsFilter(FilterBase):
    """Oscars Best filter"""

    init_with_category = False

    categories: tuple[str] = (
        "Best Picture",
        "Best Cinematography",
        "Best Original Score",
        "Nominations - Best Picture",
        "Nominations - Best Cinematography",
    )

    def __init__(
        self,
        category: t.Literal[
            "Best Picture",
            "Best Cinematography",
            "Best Original Score",
            "Nominations - Best Picture",
            "Nominations - Best Cinematography",
        ] = "Best Picture",
    ):
        """Initializes `OscarsFilter`

        Args:
            category (t.Literal[
              "Best Picture",
              "Best Cinematography",
              "Best Original Score",
              "Nominations - Best Picture",
              "Nominations - Best Cinematography"],
              optional): Oscars' award category. Defaults to "Best Picture".
        """
        assert_membership(category, self.categories)
        self.url = get_absolute_url(f"/oscars.php?category=Oscars {category}")


class MostDownloadedFilter(FilterBase):
    """Most downloaded filter"""

    init_with_arg = False

    def __init__(self, category: t.Literal["Bollywood", "Hollywood"] = "Hollywood"):
        """Initialize `MostDownloadedFilter`

        Args:
            category (t.Literal["Bollywood", "Hollywood"], optional): Movie category. Defaults to "Hollywood".
        """
        assert_membership(category, tuple(category_id_map.keys()), "Category")
        self.url = get_absolute_url(
            f"/movieslist.php?catID={category_id_map[category]}&by=downloads"
        )


class RecentlyReleasedFilter(FilterBase):
    """Recently released movies filter"""

    init_with_arg = False

    def __init__(self, category: t.Literal["Bollywood", "Hollywood"] = "Hollywood"):
        """Initialize `RecentlyReleasedFilter`

        Args:
            category (t.Literal["Bollywood", "Hollywood"], optional): Movie category. Defaults to "Hollywood".
        """
        assert_membership(category, tuple(category_id_map.keys()), "Category")
        self.url = get_absolute_url(
            f"/movieslist.php?catID={category_id_map[category]}&by=date"
        )


class RecentlyPublishedFilter(FilterBase):
    """Recently added movies"""

    init_with_arg = False

    def __init__(self, category: t.Literal["Bollywood", "Hollywood"] = "Hollywood"):
        """Initialize `RecentlyPublishedFilter`

        Args:
            category (t.Literal["Bollywood", "Hollywood"], optional): Movie category. Defaults to "Hollywood".
        """
        assert_membership(category, tuple(category_id_map.keys()), "Category")
        self.url = get_absolute_url(
            f"/movieslist.php?catID={category_id_map[category]}&by=latest"
        )


class AlphabeticalOrderFilter(FilterBase):
    """Movie name Alphabetical order filter"""

    available_ranges = (
        "AtoC",
        "DtoC",
        "GtoI",
        "JtoL",
        "MtO",
        "PtoR",
        "StoU",
        "VtoZ",
        "1to9",
    )

    def __init__(
        self,
        range: t.Literal[
            "AtoC", "DtoC", "GtoI", "JtoL", "MtO", "PtoR", "StoU", "VtoZ", "1to9"
        ] = "AtoC",
        category: t.Literal["Bollywood", "Hollywood"] = "Hollywood",
    ):
        """Initializes `AlphabeticalOrderFilter`

        Args:
            range (t.Literal["AtoC","DtoC","GtoI","JtoL","MtO","PtoR","StoU","VtoZ","1to9"], optional): Alphabetical ranges. Defaults to "AtoC".
            category (t.Literal["Bollywood", "Hollywood"], optional): Movie category. Defaults to "Hollywood".
        """
        assert_membership(range, self.available_ranges)
        assert_membership(category, category_id_map)
        self.url = get_absolute_url(
            f"/alpha.php?range={range}&catID={category_id_map[category]}"
        )


class MovieGenreFilter(FilterBase):
    """Movies for a specific genre filter"""

    available_genres = (
        "Action",
        "Adventure",
        "Animation",
        "Biography",
        "Comedy",
        "Crime",
        "Documentary",
        "Drama",
        "Family",
        "Fantasy",
        "Film-Noir",
        "History",
        "Horror",
        "Music",
        "Musical",
        "Mystery",
        "Romance",
        "Sci-Fi",
        "Sport",
        "Thriller",
        "War",
        "Western",
    )

    def __init__(
        self,
        name: t.Literal[
            "Action",
            "Adventure",
            "Animation",
            "Biography",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Family",
            "Fantasy",
            "Film-Noir",
            "History",
            "Horror",
            "Music",
            "Musical",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Sport",
            "Thriller",
            "War",
            "Western",
        ] = "Action",
        category: t.Literal["Bollywood", "Hollywood"] = "Hollywood",
    ):
        """Initialize `MovieGenreFilter`

        Args:
            name (t.Literal['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music',
            'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'], optional):
            Movie genre name. Defaults to "Action".
            category (t.Literal["Bollywood", "Hollywood"], optional): Movie category. Defaults to "Hollywood".
        """
        assert_membership(name, self.available_genres, "Genre")
        assert_membership(category, tuple(category_id_map.keys()))
        self.url = get_absolute_url(
            f"/genre.php?catID={category_id_map[category]}&genre={name}"
        )


class ReleaseYearFilter(FilterBase):
    """Movie releasal year filter"""

    def __init__(
        self,
        year: int = int(datetime.now().year),
        category: t.Literal["Bollywood", "Hollywood"] = "Hollywood",
    ):
        """Initialize `ReleaseYearFilter`

        Args:
            year (int, optional): Movie releasal year. Defaults to `datetime.now().year`
            category (t.Literal["Bollywood", "Hollywood"], optional): Movie category. Defaults to "Hollywood".
        """
        assert isinstance(int(year), int), "Year must be an Integer"
        assert_membership(category, tuple(category_id_map.keys()), "Category")
        self.url = get_absolute_url(
            f"/year.php?year={year}&catID={category_id_map[category]}"
        )


class MovieTagFilter(FilterBase):
    """Movie tag filter"""

    init_with_category = False

    def __init__(self, tag: str):
        """Initializes `MovieTagFilter`

        Args:
            tag (str): Tag name
        """
        assert isinstance(tag, str), f"Tag must be of {str} not {type(tag)}"
        self.url = get_absolute_url(f"/movietags.php?tag={tag}")


class SearchNavigatorFilter(FilterBase):
    """Navigates movie-listing-page"""

    init_with_category = False

    targets = ["first", "previous", "next", "last"]

    def __init__(
        self,
        search_results: models.SearchResults,
        target: t.Literal["first", "previous", "next", "last"] = "next",
    ):
        """Initializes `SearchNavigatorFilter`

        Args:
            search_results (models.SearchResults): Search results.
            target (t.Literal["first", "previous", "next", "last"]): Page to navigate to. Defaults to "next".
        """
        assert isinstance(search_results, models.SearchResults), (
            f"search_results should be an instance of  {models.SearchResults}"
            f" not {type(search_results)}"
        )
        assert target in self.targets, f"Target must be one of {self.targets}"
        target_url_mapper = {
            "first": search_results.first_page,
            "previous": search_results.previous_page,
            "next": search_results.next_page,
            "last": search_results.last_page,
        }
        self.url = target_url_mapper[target]
        if self.url is None:
            raise errors.TargetPageURLNotFound(
                f"The targeted page, {target}, has no url"
            )


fzmoviesFilterType = t.Union[
    IMDBTop250Filter,
    OscarsFilter,
    RecentlyPublishedFilter,
    RecentlyReleasedFilter,
    AlphabeticalOrderFilter,
    MovieGenreFilter,
    ReleaseYearFilter,
    MovieTagFilter,
    MostDownloadedFilter,
    SearchNavigatorFilter,
]
