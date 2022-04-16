import typer

from nautilus_namecodes.format.filename_console import FilenameConsoleOutput

filename_app = typer.Typer()


@filename_app.command()
def schema() -> None:
    """Output Json Schema for Filename Data"""

    typer.echo(FilenameConsoleOutput.generate_json_schema())


if __name__ == "__main__":
    filename_app()
