import click
import rich
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
    help="Filename under which to save the movie contents",
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
    help="Chunk_size for downloading movie files in KB - 512",
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


class EntryGroup:

    @fzmovies.group()
    def support():
        """Provides helpful info such as FAQs and release formats"""
        pass


class Support_:
    """Contains support info such as FAQs and release formats"""

    @staticmethod
    @click.command()
    def release_formats():
        """Show movie release formats and their descriptions"""
        from fzmovies_api import Support
        from rich.table import Table

        awesome_table = Table(show_lines=True, title="Movie Release Formats".title())

        awesome_table.add_column("Index", justify="center", style="yellow")
        awesome_table.add_column("Format", justify="left", style="cyan")
        awesome_table.add_column("Description", justify="left", style="cyan")

        for index, key_value in enumerate(
            Support.get_movie_release_formats().items(), start=1
        ):
            format, description = key_value
            awesome_table.add_row(str(index), format, description)

        rich.print(awesome_table)

    @click.command()
    def FAQs():
        """Show FAQs and their answers"""
        from fzmovies_api import Support
        from rich.table import Table

        awesome_table = Table(show_lines=True, title="FAQs and Answers".title())

        awesome_table.add_column("Index", justify="center", style="yellow")
        awesome_table.add_column("Question", justify="left", style="cyan")
        awesome_table.add_column("Answer", justify="left", style="cyan")

        for index, key_value in enumerate(
            Support.get_frequently_asked_questions().items(), start=1
        ):
            question, answer = key_value
            awesome_table.add_row(str(index), question, answer)

        rich.print(awesome_table)


def main():
    """Console entry point"""
    try:
        fzmovies.add_command(download)
        EntryGroup.support.add_command(Support_.release_formats)
        EntryGroup.support.add_command(Support_.FAQs)
        fzmovies()
    except Exception as e:
        print(f"> Error : {e.args[1] if e.args and len(e.args)>1 else e}")
        exit(1)


if __name__ == "__main__":
    main()
