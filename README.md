<h1 align="center">fzmovies-api</h1>

<p align="center">
<a href="#"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/fzmovies-api"/></a>
<a href="https://github.com/Simatwa/fzmovies-api/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/fzmovies-api/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
<a href="LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=GNUv3&label=License"/></a>
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
Auto(query="Jason Statham", searchby="Starcast").run()
```

## Installation

```
$ pip install fzmovies-api[all]
```

## Usage

### CLI

- Basic case yet very handy

   ```sh
   $ python -m fzmovies_api download <QUERY>
   # e.g python -m fzmovies_api download "Thor - Love and Thunder"
   ```

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

> ![NOTE]
> Shorthand for `python -m fzmovies_api` is `fzmovies`


## Disclaimer

This project is not affiliated with or endorsed by fzmovies.net or its owners. The API may change without notice, and this project does not guarantee compatibility with all future updates. The developers of this project are not responsible for any damages or losses resulting from the use of this API. This project is provided AS IS, without warranty of any kind, express or implied.
