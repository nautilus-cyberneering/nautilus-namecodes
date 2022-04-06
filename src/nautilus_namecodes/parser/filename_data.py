"""Encode and Decode a Filename"""

from typing import List, Optional

from nautilus_namecodes.namecodes_dataclasses import AllCodes
from nautilus_namecodes.scheme.v_0_1_0.filename import (
    Base,
    BaseAlternative,
    BaseAlternativeVairant,
    BaseVariant,
    DataType,
    Extention,
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
from nautilus_namecodes.scheme.v_0_1_0.namecode_lookup import NamecodeLookup
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
extention: Extention

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

extention = Extention("test.wonderful")

filename = Filename(library_entry, listing, info_base, data_type, extention)

print(library_entry.get_formatted_entry_string())
print(listing.get_codes(all_codes))
print(info_base.get_codes_r(all_codes))
print(data_type.get_codes(all_codes))

filename_test: str = filename.get_filename(all_codes)
print(filename_test)

model: NautilusNamecodesFilenameBaseModel = NautilusNamecodesFilenameBaseModel(
    encoding=filename
)

# print(model.schema_json())
print(model.json())


filename_test_split: List[str] = filename_test.split("-")

filename_codes_split: List[str] = filename_test_split[1].split(".")

print(filename_codes_split)

edition_code = filename_codes_split[0]

# print(all_codes.codes)

lookups: List[NamecodeLookup] = []
extention2: Extention

extentions: List[str] = []

ext_part: bool = False
for namecode in filename_codes_split:
    if ext_part is False:
        lookups.append(NamecodeLookup(all_codes, int(namecode)))
        if lookups[-1].plane == "DATATYPE":
            ext_part = True  # pylint: disable="invalid-name"

    else:
        extentions.append(namecode)


extention2 = Extention(".".join(extentions))
print(extention2)

for lookup in lookups:
    print(lookup)
