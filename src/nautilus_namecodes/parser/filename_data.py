"""Encode and Decode a Filename"""

from typing import Dict, List, Literal, Tuple, Union

from nautilus_namecodes.namecodes_dataclasses import AllCodes
from nautilus_namecodes.scheme.v_0_1_0.filename import (
    Base,
    BaseAlternative,
    BaseAlternativeVariant,
    BaseVariant,
    DataType,
    Extension,
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


class MakeFilenameTest:
    """Creates a Filename"""

    all_codes: AllCodes = NautilusNamecodesModel(data=AllNameCodes().get_all_codes).data

    gold: Gold = Gold("Gold")

    ## Note, modifications type is ignored because of pydantic bug.

    gold_base_var: Gold = Gold(
        Base(
            BaseVariant(
                Modifications(  # type: ignore
                    [
                        Modification("Adaption", "focus", "background"),
                    ]
                ),
            )
        )
    )

    gold_alt_base_alt_var: Gold = Gold(
        GoldAlternative(
            Modifications(  # type: ignore
                [
                    Modification("Adaption", "focus", "background"),
                ]
            ),
            BaseAlternative(
                BaseAlternativeVariant(
                    Modifications(  # type: ignore
                        [
                            Modification("Adaption", "prospective", "bottom"),
                        ]
                    )
                )
            ),
        )
    )

    library_entry = LibraryEntry(LibraryName("aaa"), ItemNumber(0x001))
    listing: Listing = Listing(0x001, 0x001)
    data_type: DataType = DataType("Index")
    extention = Extension("test.time")

    filename_gold: Filename = Filename(
        library_entry, listing, gold, data_type, extention
    )
    filename_gold_base_var: Filename = Filename(
        library_entry, listing, gold_base_var, data_type, extention
    )
    filename_gold_alt_base_alt_var: Filename = Filename(
        library_entry, listing, gold_alt_base_alt_var, data_type, extention
    )

    def get_test_filenames_dataclass(self) -> List[Filename]:
        """Gets the filenames for testing."""

        return [
            self.filename_gold,
            self.filename_gold_base_var,
            self.filename_gold_alt_base_alt_var,
        ]

    def get_test_filename_models(self) -> List[NautilusNamecodesFilenameBaseModel]:
        """Return Verified Pydantic Model"""

        return [
            NautilusNamecodesFilenameBaseModel(encoding=filename)
            for filename in self.get_test_filenames_dataclass()
        ]

    def get_test_filename_json(self) -> List[str]:
        """Return Json from Model"""
        return [model.json() for model in self.get_test_filename_models()]

    def get_test_filename_encoded(self) -> List[str]:
        """Return Encoded Filename"""
        return [
            filename.get_filename(self.all_codes)
            for filename in self.get_test_filenames_dataclass()
        ]


class ParseFilenameTest:  # pylint: disable=too-few-public-methods
    """Filename to model."""

    all_codes: AllCodes = NautilusNamecodesModel(data=AllNameCodes().get_all_codes).data

    make_filename_test: MakeFilenameTest = MakeFilenameTest()
    test_filenames: List[str] = make_filename_test.get_test_filename_encoded()

    filenames: List[Filename] = []

    for test_filename in test_filenames:

        # Library Name
        library_name: LibraryName = LibraryName(test_filename.split("-").pop(0)[:4])

        # Item Number
        item_number: ItemNumber = ItemNumber(
            int(test_filename.split("-")[0][4:], 16) - 0x100000
        )

        ## Library Entry
        library_entry = LibraryEntry(library_name, item_number)

        data: List[str] = test_filename.split("-", maxsplit=1)[1].split(".")

        lookups: List[NamecodeLookup] = []
        extentions: List[str] = []

        ## Extensions
        while True:
            lookups.append(NamecodeLookup(all_codes, int(data.pop(0))))
            if lookups[-1].plane == "DATATYPE":
                extentions = data
                break

        extention: Extension = Extension(".".join(extentions))

        # Listing Edition
        listing_edition_lookup: NamecodeLookup = lookups.pop(0)
        if listing_edition_lookup.plane != "LISTING":
            if listing_edition_lookup.block != "Edition":
                if listing_edition_lookup.section != "edition":
                    raise KeyError(listing_edition_lookup)

        listing_edition: int = int(listing_edition_lookup.codename.lstrip("edition: #"))

        # Listing Revision
        revision_edition_lookup: NamecodeLookup = lookups.pop(0)
        if revision_edition_lookup.plane != "LISTING":
            if revision_edition_lookup.block != "Edition":
                if revision_edition_lookup.section != "edition":
                    raise KeyError(revision_edition_lookup)

        listing_revision: int = int(
            revision_edition_lookup.codename.lstrip("revision: #")
        )

        ## Listing
        listing: Listing = Listing(listing_edition, listing_revision)

        ## Data Type
        data_types: Dict[
            str, Union[Literal["Index"], Literal["Metadata"], Literal["Media"]]
        ] = {"index": "Index", "metadata": "Metadata", "media": "Media"}

        data_type_lookup: NamecodeLookup = lookups.pop(-1)
        if data_type_lookup.plane != "DATATYPE":
            if data_type_lookup.block != "DataType":
                if data_type_lookup.section != "datatype":
                    raise KeyError(data_type_lookup)

        data_type: DataType = DataType(data_types[data_type_lookup.codename])

        gold_or_gold_alternative_or_base: Union[
            Literal["Gold"], Literal["GoldAlternative"], Literal["Base"]
        ]
        gold_alternative_or_base_alternative: Union[
            Literal["GoldAlternative"], Literal["BaseAlternative"]
        ]
        base_alternative_or_base_alternative_variant: Union[
            Literal["BaseAlternative"], Literal["BaseAlternativeVariant"]
        ]
        base_or_base_variant: Union[Literal["Base"], Literal["BaseVariant"]]

        gold_alternative_modifications: Modifications
        base_alternative_variant_modifications: Modifications
        base_variant_modifications: Modifications

        mod_mock: Modifications = Modifications(  # type: ignore
            [
                Modification("Adaption", "focus", "background"),
            ]
        )

        gold_way: Tuple[int, str] = Gold("Gold").get_codes(all_codes)[-1]
        gold_alternative_way = GoldAlternative(mod_mock, "GoldAlternative").get_codes(
            all_codes
        )[-1]
        base_alternative_way = BaseAlternative("BaseAlternative").get_codes(all_codes)[
            -1
        ]
        base_alternative_variant_way = BaseAlternativeVariant(mod_mock).get_codes(
            all_codes
        )[-1]
        base_way = Base("Base").get_codes(all_codes)[-1]
        base_variant_way = BaseVariant(mod_mock).get_codes(all_codes)[-1]

        # We must start with Gold
        if gold_way != lookups[-1].code:
            raise KeyError(lookups[-1])

        while lookups:
            lookup: NamecodeLookup = lookups.pop(-1)

            modification_lookup: NamecodeLookup
            modification_list: List[Modification] = []

            ## Gold
            if lookup.code == gold_way:
                if not lookups:
                    gold_or_gold_alternative_or_base = "Gold"
                    continue

                if lookups[-1].code == gold_alternative_way:
                    gold_or_gold_alternative_or_base = "GoldAlternative"
                    continue

                if lookups[-1].code == base_way:
                    gold_or_gold_alternative_or_base = "Base"
                    continue

                raise KeyError(
                    f"After {lookup}, {lookups[-1]} must be Empty, Gold Alternative, or Base."
                )

            ## Gold Alternative
            if lookup.code == gold_alternative_way:
                if not lookups:
                    raise KeyError(f"Must have at least one modification for {lookup}")

                if lookups[-1].plane != "MODIFICATION":
                    raise KeyError(
                        f"next {lookups[-1]} must be a modification for {lookup}"
                    )

                while lookups:
                    if lookups[-1].plane != "MODIFICATION":
                        break

                    modification_lookup = lookups.pop(-1)
                    modification_list.append(
                        Modification(
                            modification_lookup.block,
                            modification_lookup.section,
                            modification_lookup.codename,
                        )
                    )

                gold_alternative_modifications = Modifications(modification_list)  # type: ignore

                if not lookups:
                    gold_alternative_or_base_alternative = "GoldAlternative"
                    continue

                if lookups[-1].code == base_alternative_way:
                    gold_alternative_or_base_alternative = "BaseAlternative"
                    continue

                raise KeyError(
                    f"After {lookup}, {lookups[-1]} must be either Empty, or a Base Alternative."
                )

            ## Base Alternative
            if lookup.code == base_alternative_way:

                if not lookups:
                    base_alternative_or_base_alternative_variant = "BaseAlternative"
                    continue

                if lookups[-1].code == base_alternative_variant_way:
                    base_alternative_or_base_alternative_variant = (
                        "BaseAlternativeVariant"
                    )
                    continue

                raise KeyError(
                    f"After {lookup}, {lookups[-1]} must be either Empty, or a Base Alternative Variant."
                )

            ## Base Alternative Variant
            if lookup.code == base_alternative_variant_way:
                if not lookups:
                    raise KeyError(f"Must have at least one modification for {lookup}")

                if lookups[-1].plane != "MODIFICATION":
                    raise KeyError(
                        f"next {lookups[-1]} must be a modification for {lookup}"
                    )

                while lookups:
                    if lookups[-1].plane != "MODIFICATION":
                        break

                    modification_lookup = lookups.pop(-1)
                    modification_list.append(
                        Modification(
                            modification_lookup.block,
                            modification_lookup.section,
                            modification_lookup.codename,
                        )
                    )

                base_alternative_variant_modifications = Modifications(modification_list)  # type: ignore

                if not lookups:
                    continue

                raise KeyError(f"After {lookup}, must be Empty!")

            ## Base
            if lookup.code == base_way:

                if not lookups:
                    base_or_base_variant = "Base"
                    continue

                if lookups[-1].code == base_variant_way:
                    base_or_base_variant = "BaseVariant"
                    continue

                raise KeyError(
                    f"After {lookup}, {lookups[-1]} must be either Empty, or a Base Variant."
                )

            ## Base Variant
            if lookup.code == base_variant_way:
                if not lookups:
                    raise KeyError(f"Must have at least one modification for {lookup}")

                if lookups[-1].plane != "MODIFICATION":
                    raise KeyError(
                        f"next {lookups[-1]} must be a modification for {lookup}"
                    )

                while lookups:
                    if lookups[-1].plane != "MODIFICATION":
                        break

                    modification_lookup = lookups.pop(-1)
                    modification_list.append(
                        Modification(
                            modification_lookup.block,
                            modification_lookup.section,
                            modification_lookup.codename,
                        )
                    )

                base_variant_modifications = Modifications(modification_list)  # type: ignore

                if not lookups:
                    continue

                raise KeyError(f"After {lookup}, must be Empty!")

            raise KeyError(f"Unknown Key {lookup}!")

        filename: Filename
        if gold_or_gold_alternative_or_base == "Gold":
            filename = Filename(
                library_entry, listing, Gold("Gold"), data_type, extention
            )

        if gold_or_gold_alternative_or_base == "GoldAlternative":
            if gold_alternative_or_base_alternative == "GoldAlternative":
                filename = Filename(
                    library_entry,
                    listing,
                    Gold(
                        GoldAlternative(
                            gold_alternative_modifications,
                            "GoldAlternative",
                        )
                    ),
                    data_type,
                    extention,
                )

            if gold_alternative_or_base_alternative == "BaseAlternative":
                if base_alternative_or_base_alternative_variant == "BaseAlternative":
                    filename = Filename(
                        library_entry,
                        listing,
                        Gold(
                            GoldAlternative(
                                gold_alternative_modifications,
                                BaseAlternative("BaseAlternative"),
                            )
                        ),
                        data_type,
                        extention,
                    )

                if (
                    base_alternative_or_base_alternative_variant
                    == "BaseAlternativeVariant"
                ):
                    filename = Filename(
                        library_entry,
                        listing,
                        Gold(
                            GoldAlternative(
                                gold_alternative_modifications,
                                BaseAlternative(
                                    BaseAlternativeVariant(
                                        base_alternative_variant_modifications
                                    ),
                                ),
                            )
                        ),
                        data_type,
                        extention,
                    )
        if gold_or_gold_alternative_or_base == "Base":
            if base_or_base_variant == "Base":
                filename = Filename(
                    library_entry,
                    listing,
                    Gold(Base("Base")),
                    data_type,
                    extention,
                )

            if base_or_base_variant == "BaseVariant":
                filename = Filename(
                    library_entry,
                    listing,
                    Gold(Base(BaseVariant(base_variant_modifications))),
                    data_type,
                    extention,
                )
        filenames.append(filename)

    def get_filenames(self) -> List[Filename]:
        """Get the filename models."""
        return self.filenames


if __name__ == "__main__":

    make_filename_test: MakeFilenameTest = MakeFilenameTest()
    make_parse_filename_test: ParseFilenameTest = ParseFilenameTest()

    print(make_filename_test.get_test_filename_encoded())
    print(make_parse_filename_test.get_filenames())
