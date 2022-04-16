"""Main Module for Command Line App"""

from typing import Optional

import typer
from typer.main import Typer

from nautilus_namecodes.app.filename_app import filename_app
from nautilus_namecodes.app.namecode_app import namecode_app

from nautilus_namecodes._version import __version__


app: Typer = typer.Typer()

app.add_typer(filename_app, name="filename")
app.add_typer(namecode_app, name="namecode")


def version_callback(value: bool) -> None:
    """Simple Callback Function to return the Version Number of the Program"""

    if value:
        typer.echo(f"Namecodes Version: {__version__}")
        raise typer.Exit()


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
