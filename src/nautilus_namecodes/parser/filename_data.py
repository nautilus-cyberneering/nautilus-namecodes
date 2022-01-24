"""Encode and Decode a Filename"""

from typing import Optional
from nautilus_namecodes.scheme.v_0_1_0.filename import (
    Base,
    BaseAlternative,
    BaseAlternativeVairant,
    BaseVairant,
    Filename,
    Gold,
    GoldAlternative,
    ItemCode,
    LibraryCode,
    Listing,
)
from nautilus_namecodes.scheme.v_0_1_0.filename_model import (
    NautilusNamecodesFilenameBaseModel,
)
from nautilus_namecodes.scheme.v_0_1_0.namecode_model import NautilusNamecodesModel
from nautilus_namecodes.scheme.v_0_1_0.namecodes import AllNameCodes


nautilus_namecodes_model = NautilusNamecodesModel(data=AllNameCodes().get_all_codes)


filename_test: str = "test"

base_alternative_vairant: Optional[BaseAlternativeVairant]

base_alternative: Optional[BaseAlternative]
alternative: Optional[GoldAlternative]

base_vairant: Optional[BaseVairant]
base: Optional[Base]

info: Gold
listing: Listing
item: ItemCode
library: LibraryCode

filename: Filename

print(nautilus_namecodes_model.schema_json())
