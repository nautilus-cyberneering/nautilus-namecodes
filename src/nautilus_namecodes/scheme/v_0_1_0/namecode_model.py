"""Pydantic Model for Nautilus Namecodes"""

from typing import Dict

import pydantic
from pydantic.fields import Field  # pylint: disable="no-name-in-module"
from pydantic.main import BaseModel  # pylint: disable="no-name-in-module"

from nautilus_namecodes.namecodes_dataclasses import AllCodes, Range, TreeStub
from nautilus_namecodes.scheme.v_0_1_0.namecodes import AllNameCodes, TreeStubGen

# Decorate the Range Class with Pydantic.
pydantic.dataclasses.dataclass(Range)  # pylint: disable="c-extension-no-member"

# pylint: disable="too-few-public-methods"


class NautilusNamecodesModel(BaseModel):
    """Pydantic Model for Nautilus Namecodes Dataclass"""

    data: AllCodes = Field(title="Namecodes Dataclass")

    class Config:  # pylint: disable="missing-class-docstring"
        title = "Nautilus Namecodes Dataclass"


class NautilusNamecodesTreeModel(BaseModel):
    """Pydantic Model for Nautilus Namecodes Stub Tree"""

    data: TreeStub = Field(title="Namecodes Dataclass")

    class Config:  # pylint: disable="missing-class-docstring"
        title = "Nautilus Namecodes Dataclass Tree"


class NautilusNamecodesListModel(BaseModel):
    """Pydantic Model for Nautilus Namecodes List"""

    namecodes: Dict[int, str] = Field(title="Namecodes")

    class Config:  # pylint: disable="missing-class-docstring"
        title = "Nautilus Namecodes List Dataclass"


if __name__ == "__main__":
    all_codes: AllCodes = AllNameCodes().get_all_codes
    tree_stub: TreeStub = TreeStubGen().tree_stub

    print(tree_stub)

    nautilus_namecodes_model = NautilusNamecodesModel(data=all_codes)
    nautilus_namecodes_tree_model = NautilusNamecodesTreeModel(data=tree_stub)
    nautilus_namecodes_list_model = NautilusNamecodesListModel(
        namecodes=all_codes.codes
    )

    print("\n\n\n\n\n\n")
    print(nautilus_namecodes_model.schema_json(indent=2))
    print(nautilus_namecodes_tree_model.schema_json(indent=2))
    print(nautilus_namecodes_list_model.schema_json(indent=2))
