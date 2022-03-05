"""Encode and Decode a Filename"""

from typing import Dict, List, Optional, Tuple

import pydantic
from nautilus_namecodes.namecodes_dataclasses import AllCodes
from nautilus_namecodes.scheme.v_0_1_0.filename import (
    Base,
    BaseAlternative,
    BaseAlternativeVairant,
    BaseVariant,
    DataType,
    Filename,
    Gold,
    GoldAlternative,
    ItemCode,
    LibraryCode,
    Listing,
    Modification,
    Modifications,
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

base_vairant: Optional[BaseVariant]
base: Optional[Base]

info: Gold
listing: Listing
item: ItemCode
library: LibraryCode

filename: Filename


modifications: Modifications = Modifications(
    [
        Modification("Adaption", "focus", "background"),
        Modification("Adaption", "prospective", "bottom"),
    ]
)

all_codes: AllCodes = nautilus_namecodes_model.data


base_alternative_vairant = BaseAlternativeVairant(modifications)

base_alternative = BaseAlternative(base_alternative_vairant)

alternative = GoldAlternative(modifications, base_alternative)

base_vairant = BaseVariant(modifications)

base_mod = Base(base_vairant)

info_alt = Gold(alternative)
info_base = Gold(base_mod)
info_gold = Gold("gold")

listing = Listing(0x001, 0x001)

item = ItemCode(0x001)

library = LibraryCode("aaa")

filename = Filename(library, item, listing, info_base, DataType("index"))


model: NautilusNamecodesFilenameBaseModel = NautilusNamecodesFilenameBaseModel(
    encoding=filename
)

print(model.schema_json())
print(model.json())
