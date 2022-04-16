import typer


def mutually_exclusive_group(size: int):
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
