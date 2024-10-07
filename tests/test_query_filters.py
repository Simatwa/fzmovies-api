import unittest
from fzmovies_api.models import SearchResults
import fzmovies_api.filters as f
from unittest import TestCase


class FiltersTestBase:

    def setUp(self):
        self.filter_class = None

    def test_html_contents(self):
        """Test fetching movies from online"""
        self.assertIsInstance(self.filter_class.get_contents(), str)

    def test_results(self):
        """Test query results modelling"""
        self.assertIsInstance(self.filter_class.get_results(), SearchResults)


class TestIMDBTop250Filter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.IMDBTop250Filter()


class TestOscarsFilter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.OscarsFilter()


class TestMostDownloadedFilter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.MostDownloadedFilter()


class TestRecentlyReleasedFilter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.RecentlyReleasedFilter()


class TestRecentlyPublishedFilter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.RecentlyPublishedFilter()


class TestAlphabeticalOrderFilter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.AlphabeticalOrderFilter()


class TestMovieGenreFilter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.MovieGenreFilter()


class TestReleaseYearFilter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.ReleaseYearFilter()


class TestMovieTagFilter(FiltersTestBase, TestCase):

    def setUp(self):
        self.filter_class = f.MovieTagFilter("Love")


class TestSearchNavigatorFilter(FiltersTestBase, TestCase):

    def setUp(self):
        search_results = f.ReleaseYearFilter(2020).get_results()
        self.filter_class = f.SearchNavigatorFilter(
            search_results,
        )


if __name__ == "__main__":
    unittest.main()
