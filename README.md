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
<a href="https://pepy.tech/project/livescore-api"><img src="https://static.pepy.tech/personalized-badge/fzmovies-api?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
<a href="https://github.com/Simatwa/fzmovies-api/releases/latest"><img src="https://img.shields.io/github/downloads/Simatwa/fzmovies-api/total?label=Asset%20Downloads&color=success" alt="Downloads"></img></a>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com/Simatwa/fzmovies-api"/></a>
</p>

> Unofficial Python API/SDK for fzmovies.net

```python
from fzmovies_api import Auto

Auto(
     query="Fast and Furious 5",
     quality="720p",
  ).run()
  
# Will show download progressbar

```

## Installation

```
$ pip install fzmovies-api[all]
```

Alternatively, you can download binaries for your system from [here](https://github.com/Simatwa/fzmovies-api/releases/latest).

## Usage

### CLI

- Basic case yet very handy

   ```sh
   $ python -m fzmovies_api download <QUERY>
   # e.g python -m fzmovies_api download "Thor - Love and Thunder"
   ```

> [!TIP]
> Shorthand for `python -m fzmovies_api` is `fzmovies`

   `$ python -m fzmovies_api download --help`

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

> [!NOTE]
> **fzmovies_api** provides a lot more than what you've just gone through here. Documenting isn't my thing, but I will try to update it as time goes by. Additionally, I cannot document this any better than the code itself; therefore, consider going through it.

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


## Disclaimer

This project is not affiliated with or endorsed by fzmovies.net or its owners. The API may change without notice, and this project does not guarantee compatibility with all future updates. The developers of this project are not responsible for any damages or losses resulting from the use of this API. This project is provided AS IS, without warranty of any kind, express or implied.
