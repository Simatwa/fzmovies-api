import unittest, os
from fzmovies_api import Search, Navigate, DownloadLinks, Download, Support
import fzmovies_api.models as models
import typing as t

search_kwargs = {"query": "Jason Statham", "searchby": "Starcast"}


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.search = Search(**search_kwargs)

    def test_fetching_html_contents(self):
        self.assertIsInstance(self.search.html_contents, str)

    def test_search_results(self):
        self.assertIsInstance(self.search.results, models.SearchResults)

    def test_all_search_results(self):
        self.assertIsInstance(
            self.search.get_all_results(limit=20), models.SearchResults
        )

    def test_limited_search_results(self):
        limit = 20
        results = self.search.get_all_results(limit=limit)
        self.assertEqual(limit, len(results.movies))

    def test_stream_all_search_results(self):
        results = self.search.get_all_results(stream=True, limit=20)
        self.assertIsInstance(results, t.Generator)
        for result in results:
            self.assertIsInstance(result, models.SearchResults)


class TestNavigate(unittest.TestCase):

    def setUp(self):
        search = Search(**search_kwargs).results
        self.navigate = Navigate(search.movies[0])

    def test_fetching_html_contents(self):
        self.assertIsInstance(self.navigate.html_contents, str)

    def test_navigate_results(self):
        self.assertIsInstance(self.navigate.results, models.MovieFiles)


class TestDownloadLinks(unittest.TestCase):
    def setUp(self):
        search = Search(**search_kwargs).results
        self.navigate = Navigate(search.movies[0]).results
        self.download_links = DownloadLinks(self.navigate.files[0])

    def test_fetching_html_contents(self):
        self.assertIsInstance(self.download_links.html_contents, str)

    def test_navigate_results(self):
        self.assertIsInstance(self.download_links.results, models.DownloadMovie)


class TestDownload(unittest.TestCase):
    def setUp(self):
        search = Search(**search_kwargs).results
        self.navigate = Navigate(search.movies[0]).results
        self.download_links = DownloadLinks(self.navigate.files[0]).results
        self.download = Download(self.download_links.links[0])

    def test_last_url(self):
        self.assertIsInstance(self.download.last_url, str)

    @unittest.skip("Downloading a movie is resource intensive")
    def test_save(self):
        saved_to = self.download.save(
            filename=self.download_links.filename, quiet=True, progress_bar=False
        )
        self.assertTrue(saved_to.is_file())
        os.remove(saved_to)


class TestSupport(unittest.TestCase):
    def setUp(self):
        pass

    def test_movie_release_formats(self):
        self.assertIsInstance(Support.get_movie_release_formats(), dict)

    def test_frequently_asked_questions(self):
        self.assertIsInstance(Support.get_frequently_asked_questions(), dict)


if __name__ == "__main__":
    unittest.main()
