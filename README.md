<h1 align="center">fzmovies-api</h1>

<p align="center">
<a href="#"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/fzmovies-api"/></a>
<a href="https://github.com/Simatwa/fzmovies-api/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/fzmovies-api/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
<a href="LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=GPLv3&label=License"/></a>
<a href="https://pypi.org/project/fzmovies-api"><img alt="PyPi" src="https://img.shields.io/pypi/v/fzmovies-api"></a>
<a href="https://github.com/Simatwa/fzmovies-api/releases"><img src="https://img.shields.io/github/v/release/Simatwa/fzmovies-api?label=Release&logo=github" alt="Latest release"></img></a>
<a href="https://github.com/Simatwa/fzmovies-api/releases"><img src="https://img.shields.io/github/release-date/Simatwa/fzmovies-api?label=Release date&logo=github" alt="release date"></img></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
<a href="https://github.com/Simatwa/fzmovies-api/actions/workflows/python-publish.yml"><img src="https://github.com/Simatwa/fzmovies-api/actions/workflows/python-publish.yml/badge.svg" alt="Python-publish"/></a>
<a href="https://pepy.tech/project/fzmovies-api"><img src="https://static.pepy.tech/personalized-badge/fzmovies-api?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
<a href="https://github.com/Simatwa/fzmovies-api/releases/latest"><img src="https://img.shields.io/github/downloads/Simatwa/fzmovies-api/total?label=Asset%20Downloads&color=success" alt="Downloads"></img></a>
<!--
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com/Simatwa/fzmovies-api"/></a>
-->
</p>

> Unofficial Python API/SDK for fzmovies.net

```python
from fzmovies_api import Auto

Auto(
     query="Fast and Furious 5",
     quality="720p",
  ).run()

# Will show download progressbar
"""
Fast_and_Furious_5_BluRay v2_720p.mkv
805 MB ██████████████████                            42%|
"""

```

## Installation

```
$ pip install fzmovies-api[all]
```

Alternatively, you can download binaries for your system from [here](https://github.com/Simatwa/fzmovies-api/releases/latest).

## Usage

<details>

<summary>
  <h3>Developers</h3>
</summary>

```python
# Search by Starcast

from fzmovies_api import Search

search = Search(
    query="Jason Statham",
    searchby="Starcast"
)

print(
    search.results
)

# Output
"""
<SearchResults movies=[<MovieInSearch title="Fast and Furious Presents - Hobbs and Shaw",year=2019> | <MovieInSearch title="Fast X",year=2023> | <MovieInSearch title="The Fate of the Furious [Part 8]",year=2017> | <MovieInSearch title="Mechanic Resurrection",year=2016> | <MovieInSearch title="The Meg",year=2018> | <MovieInSearch title="Wrath of Man",year=2021> | <MovieInSearch title="The Beekeeper",year=2024> | <MovieInSearch title="Operation Fortune Ruse de guerre",year=2023> | <MovieInSearch title="The Expendables 2",year=2012> | <MovieInSearch title="The Expendables 3",year=2014> | <MovieInSearch title="Meg 2 The Trench",year=2023> | <MovieInSearch title="Homefront",year=2013> | <MovieInSearch title="Parker",year=2013> | <MovieInSearch title="Safe",year=2012> | <MovieInSearch title="The Expendables 1",year=2010> | <MovieInSearch title="The Transporter 2002",year=2002> | <MovieInSearch title="Transporter 3 2008",year=2008> | <MovieInSearch title="Death Race",year=2008> | <MovieInSearch title="Expend4bles",year=2023> | <MovieInSearch title="Transporter 2 2005",year=2005>]>
"""
```

#### Perform Search Using Filters

```python
from fzmovies_api import Search
from fzmovies_api.filters import IMDBTop250Filter

search = Search(
    query = IMDBTop250Filter()
)

print(
    search.results
)


#Output
"""
<SearchResults movies=[<MovieInSearch title="Schindlers List",year=1993> | <MovieInSearch title="The Godfather - Part 1",year=1972> | <MovieInSearch title="Pulp Fiction",year=1994> | <MovieInSearch title="12 Angry Men",year=1957> | <MovieInSearch title="Terminator 2 Judgment Day",year=1991> | <MovieInSearch title="The Avengers",year=2012> | <MovieInSearch title="The Cold Light of Day",year=2012> | <MovieInSearch title="The Good the Bad and the Ugly",year=1966> | <MovieInSearch title="The Shawshank Redemption",year=1994> | <MovieInSearch title="Raging Bull",year=1980> | <MovieInSearch title="The Lion King",year=1994> | <MovieInSearch title="New Gladiators",year=2002> | <MovieInSearch title="The Dictator",year=2012> | <MovieInSearch title="The Matrix",year=1999> | <MovieInSearch title="Heat",year=1995> | <MovieInSearch title="2001 A Space Odyssey",year=1968> | <MovieInSearch title="The Silence of the Lambs",year=1991> | <MovieInSearch title="The Departed",year=2006> | <MovieInSearch title="Braveheart",year=1995> | <MovieInSearch title="Up",year=2009>]>
"""
```

#### Fetch All Search Results

```python
from fzmovies_api import Search
from fzmovies_api.filters import IMDBTop250Filter

search = Search(
    query = IMDBTop250Filter()
)

print(
    search.all_results
)

```

##### Limit movies and stream results

```python
from fzmovies_api import Search
from fzmovies_api.filters import MovieGenreFilter

search = Search(
    query = MovieGenreFilter(
        "Action"
    )
)

for result in search.get_all_results(
    limit=40,
    stream=True
    ):

    print(
        result, end='\n\n'
    )
```

#### Download Movies

```python
from fzmovies_api import Search, Navigate, DownloadLinks, Download
from fzmovies_api.filters import OscarsFilter

search = Search(
    query=OscarsFilter(
        category="Best Picture"
    )
)

for movie in search.all_results.movies:

    # Navigate to the specific movie-page
    movie_page = Navigate(movie).results

    # Go to page containing download link
    download_link_page = DownloadLinks(
        movie_page.files[1]
    )

    download_link_metadata = download_link_page.results

    # Follow the link to download the movie
    download_movie = Download(
        download_link_metadata.links[0]
    )

    print(
        "Downloading : '" + movie.title + "' of size " + download_link_metadata.size
    )

    # Dowload the movie using save method
    saved_to = download_movie.save(
        download_link_metadata.filename,
        # To silence progressbar & any other stdout:
        # progress_bar = False,
        # quiet = True
    )

    print(
        saved_to
    )
```

##### Using Auto

```python
from fzmovies_api import Auto
from fzmovies_api.filters import RecentlyReleasedFilter

start = Auto(
    query=RecentlyReleasedFilter(
        category="Hollywood"
    )
)

start.run()
```


</details>

### CLI

- Basic case yet very handy

   ```sh
   $ python -m fzmovies_api download <QUERY>
   # e.g python -m fzmovies_api download "Thor - Love and Thunder"
   ```

> [!TIP]
> Shorthand for `python -m fzmovies_api` is `fzmovies`

<details>

<summary>
   <code>$ fzmovies download --help</code>
</summary>

```
Usage: python -m fzmovies_api download [OPTIONS] QUERY

  Perform search and download first movie in the search results

Options:
  -s, --searchby [Name|Director|Starcast]
                                  Query search-by filter - Name
  -c, --category [All|Bollywood|Hollywood|DHollywood]
                                  Query movie category - All
  -q, --quality [480p|720p]       Movie file download quality - 720p
  -o, --output TEXT               Filename for saving the movie contents to
  -d, --directory TEXT            Directory for saving the movie contents -
                                  pwd
  -z, --chunk-size INTEGER        Chunk_size for downloading files in KB - 512
  -r, --resume                    Resume downloading incomplete files - False
  -q, --quiet                     Not to stdout anything - False
  -y, --yes                       Okay to all prompts - False
  --help                          Show this message and exit.

```

</details>

> [!NOTE]
> **fzmovies_api** provides a lot more than what you've just gone through here. Documenting isn't my thing, but I will try to update it as time goes by. Additionally, I cannot document this any better than the code itself; therefore, consider going through it.

## Disclaimer

This project is not affiliated with or endorsed by fzmovies.net or its owners. The API may change without notice, and this project does not guarantee compatibility with all future updates. The developers of this project are not responsible for any damages or losses resulting from the use of this API. This project is provided AS IS, without warranty of any kind, express or implied.
