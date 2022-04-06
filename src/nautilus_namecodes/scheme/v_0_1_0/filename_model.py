"""Dataclass for the Data Encoded into a Namecode Filename"""

from pydantic import BaseModel  # pylint: disable="no-name-in-module"
from pydantic.fields import Field  # pylint: disable="no-name-in-module"

from nautilus_namecodes.scheme.v_0_1_0.filename import Filename

# pylint: disable="too-few-public-methods"


class NautilusNamecodesFilenameBaseModel(BaseModel):
    """Pydantic Model for Nautilus Namecodes Filename"""

    encoding: Filename = Field(title="Filename")

    class Config:  # pylint: disable="missing-class-docstring"
        title = "Nautilus Namecodes Filename Dataclass"


if __name__ == "__main__":

    print(NautilusNamecodesFilenameBaseModel.schema_json())

    # nautilus_namecodes_model = NautilusNamecodesFilenameBaseModel()

    # print("\n\n\n\n\n\n")
    # print(nautilus_namecodes_model.schema_json(indent=2))
