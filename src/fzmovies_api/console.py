import click
import rich
from os import getcwd
from sys import exit
from fzmovies_api import __repo__, __version__
from fzmovies_api.hunter import Index
from fzmovies_api.utils import file_index_quality_map

movie_search_filters: tuple[str] = (
    "IMDBTop250",
    "Oscars",
    "RecentlyPublished",
    "RecentlyReleased",
    "AlphabeticalOrder",
    "MovieGenre",
    "ReleaseYear",
    "MovieTag",
    "MostDownloaded",
)


@click.group(epilog=f"Repository : {__repo__}")
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
    "-C",
    "--color",
    help="Progressbar color - cyan",
    default="cyan",
)
@click.option(
    "--trace/--no-trace",
    help="Do not keep traces of the progressbar upon completion - True",
    default=True,
)
@click.option(
    "-r", "--resume", is_flag=True, help="Resume downloading incomplete files - False"
)
@click.option(
    "-S", "--simple", is_flag=True, help="Show percentage and bar only in progressbar"
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
    color,
    trace,
    resume,
    simple,
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
        leave=trace,
        colour=color,
        simple=simple,
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


class Search:
    """Discover movies"""

    @staticmethod
    @click.command()
    @click.argument("query", required=False)
    @click.option(
        "-b",
        "--by",
        help="Search category - Name",
        type=click.Choice(["Name", "Director", "Starcast"]),
        default="Name",
    )
    @click.option(
        "-c",
        "--category",
        help="Search category - All",
        type=click.Choice(["All", "Bollywood", "Hollywood", "DHollywood"]),
        default="All",
    )
    @click.option(
        "-f",
        "--filter",
        help="Movie search filter name",
        type=click.Choice(movie_search_filters),
        metavar="[" + "|".join(movie_search_filters[:3]) + "|...]",
    )
    @click.option(
        "-o",
        "--output",
        help="Path to save the results in json format.",
        type=click.Path(dir_okay=False, resolve_path=True, exists=False),
    )
    @click.option("-v", "--value", help="Filter argument value if needed")
    @click.option(
        "-l",
        "--limit",
        type=click.INT,
        help="Maximum number of movies to be listed - 1_000_000",
        default=1_000_000,
    )
    @click.option("-q", "--quiet", is_flag=True, help="Do not stdout formatted table.")
    def discover(query, by, category, filter, output, value, limit, quiet):
        """Explore movies by query or filter"""
        from fzmovies_api import Search
        from fzmovies_api.filters import (
            IMDBTop250Filter,
            OscarsFilter,
            RecentlyPublishedFilter,
            RecentlyReleasedFilter,
            AlphabeticalOrderFilter,
            MovieGenreFilter,
            ReleaseYearFilter,
            MovieTagFilter,
            MostDownloadedFilter,
            fzmoviesFilterType,
        )

        filter_obj_map: dict[str, fzmoviesFilterType] = dict(
            zip(
                movie_search_filters,
                (
                    IMDBTop250Filter,
                    OscarsFilter,
                    RecentlyPublishedFilter,
                    RecentlyReleasedFilter,
                    AlphabeticalOrderFilter,
                    MovieGenreFilter,
                    ReleaseYearFilter,
                    MovieTagFilter,
                    MostDownloadedFilter,
                ),
            )
        )

        assert (
            query != None and filter != None
        ) == False, f"Only QUERY or FILTER is required. Not all of them."

        if query:
            assert value is None, (
                f"Filter value like '{value}' is only required "
                "when performing search using filters and not "
                "bare query."
            )
            search = Search(query, by, category)
        elif filter:
            filter_obj = filter_obj_map[filter]
            filter_obj_kwargs = {
                "category": category,
            }
            if filter_obj.init_with_arg:
                assert (
                    value
                ), f"Filter '{filter}' requires an argument. Use -v/--value to pass it."
                if filter_obj.init_with_category:
                    search = Search(filter_obj(value, category))
                else:
                    search = Search(filter_obj(value))
            else:
                if filter_obj.init_with_category:
                    search = Search(filter_obj(category))
                else:
                    search = Search(filter_obj())
        else:
            raise Exception(
                "A search query/filter is required. Check usage message for more info."
            )
        import rich
        from rich.table import Table

        page_no = total = 0
        results_cache: list[dict[str, str | int]] = []
        search_str = f"{query or filter}{ '('+value+')' if value else ''}"
        for s in search.get_all_results(stream=True, limit=limit):
            page_no += 1
            awesome_table = Table(
                show_lines=True,
                title=f"Search {search_str} (Page. {page_no})",
            )
            awesome_table.add_column("Index", justify="center", style="yellow")
            awesome_table.add_column("Title", justify="left", style="cyan")
            awesome_table.add_column("Year", justify="left", style="cyan")
            awesome_table.add_column("Description", justify="left", style="cyan")
            for movie in s.movies:
                if output:
                    results_cache.append(
                        dict(title=movie.title, year=movie.year, about=movie.about)
                    )
                total += 1
                awesome_table.add_row(
                    str(total), movie.title, str(movie.year), movie.about
                )
            if not quiet:
                rich.print(awesome_table)

        if output and results_cache:
            from json import dump

            if not str(output).endswith(".json"):
                output = str(output) + ".json"

            with open(output, "w") as fh:
                dump(
                    dict(
                        search=search_str,
                        filter=dict(name=filter, value=value),
                        total=len(results_cache),
                        movies=results_cache,
                    ),
                    fh,
                    indent=4,
                )


def main():
    """Console entry point"""
    try:
        fzmovies.add_command(download)
        fzmovies.add_command(Search.discover)
        EntryGroup.support.add_command(Support_.release_formats)
        EntryGroup.support.add_command(Support_.FAQs)
        fzmovies()
    except Exception as e:
        print(f"> Error : {e.args[1] if e.args and len(e.args)>1 else e}")
        exit(1)


if __name__ == "__main__":
    main()
