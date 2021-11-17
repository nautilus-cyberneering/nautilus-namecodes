"""Main Module for Command Line App"""

from typing import Optional

import typer
from typer.main import Typer

from nautilus_namecodes._version import __version__
from nautilus_namecodes.format.generate_console import ConsoleOutput

app: Typer = typer.Typer()


def mutually_exclusive_group(size=2):
    """Helper Function to assure Mutually Exclusive Options are not used."""

    group = set()

    def callback(
        ctx: typer.Context, param: typer.CallbackParam, value: bool
    ):  # pylint: disable=unused-argument
        # Add cli option to group if it was called with a value
        if value is not None and param.name not in group:
            group.add(param.name)
        if len(group) > size - 1:
            raise typer.BadParameter(f"{group} are mutually exclusive")
        return value

    return callback


def version_callback(value: bool) -> None:
    """Simple Callback Function to return the Version Number of the Program"""

    if value:
        typer.echo(f"Namecodes Version: {__version__}")
        raise typer.Exit()


exclusivity_callback = mutually_exclusive_group()


@app.command()
def codes(
    show_all: bool = typer.Option(
        None,
        "--show-all",
        help="Print All Codes to Console.",
        callback=exclusivity_callback,
    ),
    show_tree: bool = typer.Option(
        None,
        "--show-tree",
        help="Print Summary Tree to Console.",
        callback=exclusivity_callback,
    ),
) -> None:
    """Command for the Management of Name Codes"""

    if not any([show_all, show_tree]):
        raise typer.BadParameter(
            "Required to specify either: --show-all or --show-tree."
        )

    if show_all:
        typer.echo(ConsoleOutput().gen_full_output())

    if show_tree:
        typer.echo(ConsoleOutput().gen_tree_output())


@app.callback()
def main(
    version: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
        None, "--version", callback=version_callback
    ),
):
    """Main Function of CLI application, defining main options."""
    return


if __name__ == "__main__":
    app()
