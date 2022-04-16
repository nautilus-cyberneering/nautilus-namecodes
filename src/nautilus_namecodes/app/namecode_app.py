import typer

from nautilus_namecodes.app._helpers_app import mutually_exclusive_group
from nautilus_namecodes.format.namecode_console import NamecodesConsoleOutput

namecode_app = typer.Typer()
namecode_show_app = typer.Typer()

format_exclusivity_callback = mutually_exclusive_group(2)


@namecode_show_app.command()
def tree(  # pylint: disable="too-many-arguments,too-many-branches"
    markdown: bool = typer.Option(
        None,
        "--markdown",
        help="Format Output as Markdown.",
        callback=format_exclusivity_callback,
    ),
    json: bool = typer.Option(
        None,
        "--json",
        help="Format Output as Json",
        callback=format_exclusivity_callback,
    ),
) -> None:
    """Command for the Management of Name Codes"""

    if not any([markdown, json]):
        typer.echo("Defaulting to Markdown output.")
        markdown = True

    if markdown:
        typer.echo(NamecodesConsoleOutput.generate_tree_output())

    if json:
        typer.echo(NamecodesConsoleOutput.generate_json_tree())


@namecode_show_app.command()
def blocks(  # pylint: disable="too-many-arguments,too-many-branches"
    markdown: bool = typer.Option(
        None,
        "--markdown",
        help="Format Output as Markdown.",
        callback=format_exclusivity_callback,
    ),
    json: bool = typer.Option(
        None,
        "--json",
        help="Format Output as Json",
        callback=format_exclusivity_callback,
    ),
) -> None:
    """Command for the Management of Name Codes"""

    if not any([markdown, json]):
        typer.echo("Defaulting to Markdown output.")
        markdown = True

    if markdown:
        typer.echo(NamecodesConsoleOutput.generate_blocks_output())

    if json:
        typer.echo(NamecodesConsoleOutput.generate_json())


@namecode_show_app.command()
def codes(  # pylint: disable="too-many-arguments,too-many-branches"
    markdown: bool = typer.Option(
        None,
        "--markdown",
        help="Format Output as Markdown.",
        callback=format_exclusivity_callback,
    ),
    json: bool = typer.Option(
        None,
        "--json",
        help="Format Output as Json",
        callback=format_exclusivity_callback,
    ),
) -> None:
    """Command for the Management of Name Codes"""

    if not any([markdown, json]):
        typer.echo("Defaulting to Markdown output.")
        markdown = True

    if markdown:
        typer.echo(NamecodesConsoleOutput.generate_codes_output())

    if json:
        typer.echo(NamecodesConsoleOutput.generate_json_codelist())


@namecode_show_app.command()
def schema() -> None:  # pylint: disable="too-many-arguments,too-many-branches"
    """Command for the Management of Name Codes"""

    typer.echo(NamecodesConsoleOutput.generate_json_schema_codelist())


namecode_app.add_typer(namecode_show_app, name="show")
