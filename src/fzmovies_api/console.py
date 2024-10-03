import click
from os import getcwd
from sys import exit
from fzmovies_api import __version__
from fzmovies_api.hunter import Index
from fzmovies_api.utils import file_index_quality_map


@click.group(epilog="This script has no any official relation with fzmovies.net")
@click.version_option(
    version=__version__,
    package_name="fzmovies_api",
    prog_name="fzmovies",
)
def fzmovies():
    """Download movies like a pro from fzmovies.net"""
    pass


@click.command()
@click.argument("query", required=True)
@click.option(
    "-s",
    "--searchby",
    help="Query search-by filter - Name",
    type=click.Choice(Index.searchby_options),
    default="Name",
)
@click.option(
    "-c",
    "--category",
    help="Query movie category - All",
    type=click.Choice(Index.category_options),
    default="All",
)
@click.option(
    "-q",
    "--quality",
    help="Movie file download quality - 720p",
    type=click.Choice(list(file_index_quality_map.keys())),
    default="720p",
)
@click.option(
    "-o",
    "--output",
    help="Filename for saving the movie contents to",
)
@click.option(
    "-d",
    "--directory",
    help="Directory for saving the movie contents - pwd",
    default=getcwd(),
)
@click.option(
    "-z",
    "--chunk-size",
    help="Chunk_size for downloading files in KB - 512",
    default=512,
    type=click.INT,
)
@click.option(
    "-r", "--resume", is_flag=True, help="Resume downloading incomplete files - False"
)
@click.option("-q", "--quiet", is_flag=True, help="Not to stdout anything - False")
@click.option("-y", "--yes", is_flag=True, help="Okay to all prompts - False")
def download(
    query: str,
    searchby: str,
    category: str,
    quality: str,
    output,
    directory,
    chunk_size,
    resume,
    quiet,
    yes,
):
    """Perform search and download first movie in the search results"""
    from fzmovies_api import Auto

    start = Auto(quality=quality, query=query, searchby=searchby, category=category)
    if yes:
        pass
    else:
        if not click.confirm(
            f'Are you sure to {"resume downloading" if resume else "download"} this movie '
            f'"{start.target.title}" - {start.target.year}'
        ):
            exit(0)

    start.run(
        filename=output,
        dir=directory,
        chunk_size=chunk_size,
        resume=resume,
        quiet=quiet,
        progress_bar=quiet == False,
    )


def main():
    """Console entry point"""
    try:
        fzmovies.add_command(download)
        fzmovies()
    except Exception as e:
        print(f"> Error : {e.args[1] if e.args and len(e.args)>1 else e}")
        exit(1)


if __name__ == "__main__":
    main()
