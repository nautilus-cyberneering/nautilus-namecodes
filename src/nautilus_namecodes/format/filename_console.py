"""Generate the Console Output for the Encoded Filename"""

from nautilus_namecodes.scheme.v_0_1_0.filename_model import (
    NautilusNamecodesFilenameBaseModel,
)


class FilenameConsoleOutput:  # pylint: disable="too-few-public-methods"
    """Generate Text Output suitable for the Console."""

    @staticmethod
    def generate_json_schema() -> str:
        """Generate Dataclass Json Schema"""

        return NautilusNamecodesFilenameBaseModel.schema_json()
