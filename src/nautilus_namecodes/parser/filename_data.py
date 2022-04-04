"""Encode and Decode a Filename"""

from typing import Dict, List, Optional

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
    ItemNumber,
    LibraryEntry,
    LibraryName,
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
all_codes: AllCodes = nautilus_namecodes_model.data

base_alternative_vairant: Optional[BaseAlternativeVairant]

base_alternative: Optional[BaseAlternative]
alternative: Optional[GoldAlternative]

base_vairant: Optional[BaseVariant]
base: Optional[Base]

info: Gold
listing: Listing
item: ItemNumber
library: LibraryName
library_entry: LibraryEntry

filename: Filename

## Note, type is ignored because of pydantic bug.
modifications: Modifications = Modifications(  # type: ignore
    [
        Modification("Adaption", "focus", "background"),
        Modification("Adaption", "prospective", "bottom"),
    ]
)

base_alternative_vairant = BaseAlternativeVairant(modifications)

base_alternative = BaseAlternative(base_alternative_vairant)

alternative = GoldAlternative(modifications, base_alternative)

base_vairant = BaseVariant(modifications)

base_mod = Base(base_vairant)

info_alt = Gold(alternative)
info_base = Gold(base_mod)
info_gold = Gold("gold")


listing = Listing(0x001, 0x001)

item = ItemNumber(0x001)

library = LibraryName("aaa")
data_type: DataType = DataType("index")

library_entry = LibraryEntry(library, item)

filename = Filename(library_entry, listing, info_base, data_type)

print(library_entry.get_formated_entry_string())
print(listing.get_codes(all_codes))
print(info_base.get_codes_r(all_codes))
print(data_type.get_codes(all_codes))

print(filename.get_filename(all_codes))

model: NautilusNamecodesFilenameBaseModel = NautilusNamecodesFilenameBaseModel(
    encoding=filename
)

# print(model.schema_json())
print(model.json())

filename_test: str = "aaa100001-256.512.1552.1590.51.50.48.0"

filename_test_split: List[str] = filename_test.split("-")
