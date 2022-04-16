"""Encode and Decode a Filename"""

from typing import Dict, List, Literal, Tuple

from nautilus_namecodes.namecodes_dataclasses import AllCodes
from nautilus_namecodes.scheme.v_0_1_0.filename import (
    DataType,
    Extension,
    Filename,
    Gold,
    GoldAlternative,
    GoldAlternativeBase,
    GoldAlternativeBaseVariant,
    GoldBase,
    GoldBaseVariant,
    ItemNumber,
    LibraryEntry,
    LibraryName,
    Listing,
    Modification,
    Modifications,
    Way,
    WayPaths,
    Ways,
)
from nautilus_namecodes.scheme.v_0_1_0.namecode_lookup import NamecodeLookup


class ParseFilename:
    """Parse an Encoded Filename"""

    ModificationsT = Dict[
        Literal[
            Ways.GOLD_ALTERNATIVE,
            Ways.GOLD_ALTERNATIVE_BASE_VARIANT,
            Ways.GOLD_BASE_VARIANT,
        ],
        Modifications,
    ]

    WayPathsModificationsT = Tuple[WayPaths, ModificationsT]

    @staticmethod
    def find_path_and_extract_modifications(  # pylint: disable="too-many-branches","too-many-statements"
        all_codes: AllCodes, lookups: List[NamecodeLookup]
    ) -> WayPathsModificationsT:
        """Finds the WayPath and Extracts the Modifications"""

        waycode: Dict[Ways, Tuple[int, str]] = {
            Ways.GOLD: Way.get_way_code(all_codes, Ways.GOLD),
            Ways.GOLD_ALTERNATIVE: Way.get_way_code(all_codes, Ways.GOLD_ALTERNATIVE),
            Ways.GOLD_ALTERNATIVE_BASE: Way.get_way_code(
                all_codes, Ways.GOLD_ALTERNATIVE_BASE
            ),
            Ways.GOLD_ALTERNATIVE_BASE_VARIANT: Way.get_way_code(
                all_codes, Ways.GOLD_ALTERNATIVE_BASE_VARIANT
            ),
            Ways.GOLD_BASE: Way.get_way_code(all_codes, Ways.GOLD_BASE),
            Ways.GOLD_BASE_VARIANT: Way.get_way_code(all_codes, Ways.GOLD_BASE_VARIANT),
        }

        waypaths = WayPaths()
        modifications: ParseFilename.ModificationsT = {}

        # We must start with Gold
        if lookups[0].code != waycode[Ways.GOLD]:
            raise KeyError(lookups[0])

        while lookups:
            lookup: NamecodeLookup = lookups.pop(0)

            modification_lookup: NamecodeLookup
            modification_list: List[Modification] = []

            ## Gold
            if lookup.code == waycode[Ways.GOLD]:
                if not lookups:
                    waypaths.gold = Ways.GOLD
                    continue

                if lookups[0].code == waycode[Ways.GOLD_ALTERNATIVE]:
                    waypaths.gold = Ways.GOLD_ALTERNATIVE
                    continue

                if lookups[0].code == waycode[Ways.GOLD_BASE]:
                    waypaths.gold = Ways.GOLD_BASE
                    continue

                raise KeyError(
                    f"After {lookup}, {lookups[-1]} must be Empty, Gold Alternative, or Base."
                )

            ## Gold Alternative
            if lookup.code == waycode[Ways.GOLD_ALTERNATIVE]:
                if not lookups:
                    raise KeyError(f"Must have at least one modification for {lookup}")

                if lookups[0].plane != "MODIFICATION":
                    raise KeyError(
                        f"next {lookups[-1]} must be a modification for {lookup}"
                    )

                while lookups:
                    if lookups[0].plane != "MODIFICATION":
                        break

                    modification_lookup = lookups.pop(0)
                    modification_list.append(
                        Modification(
                            modification_lookup.block,
                            modification_lookup.section,
                            modification_lookup.codename,
                        )
                    )

                modifications[Ways.GOLD_ALTERNATIVE] = Modifications(modification_list)  # type: ignore

                if not lookups:
                    waypaths.gold_alternative = Ways.GOLD_ALTERNATIVE
                    continue

                if lookups[0].code == waycode[Ways.GOLD_ALTERNATIVE_BASE]:
                    waypaths.gold_alternative = Ways.GOLD_ALTERNATIVE_BASE
                    continue

                raise KeyError(
                    f"After {lookup}, {lookups[-1]} must be either Empty, or a Base Alternative."
                )

            ## Base Alternative
            if lookup.code == waycode[Ways.GOLD_ALTERNATIVE_BASE]:

                if not lookups:
                    waypaths.gold_alternative_base = Ways.GOLD_ALTERNATIVE_BASE
                    continue

                if lookups[0].code == waycode[Ways.GOLD_ALTERNATIVE_BASE_VARIANT]:
                    waypaths.gold_alternative_base = Ways.GOLD_ALTERNATIVE_BASE_VARIANT
                    continue

                raise KeyError(
                    f"After {lookup}, {lookups[0]} must be either Empty, or a Base Alternative Variant."
                )

            ## Base Alternative Variant
            if lookup.code == waycode[Ways.GOLD_ALTERNATIVE_BASE_VARIANT]:
                if not lookups:
                    raise KeyError(f"Must have at least one modification for {lookup}")

                if lookups[0].plane != "MODIFICATION":
                    raise KeyError(
                        f"next {lookups[-1]} must be a modification for {lookup}"
                    )

                while lookups:
                    if lookups[0].plane != "MODIFICATION":
                        break

                    modification_lookup = lookups.pop(0)
                    modification_list.append(
                        Modification(
                            modification_lookup.block,
                            modification_lookup.section,
                            modification_lookup.codename,
                        )
                    )

                modifications[Ways.GOLD_ALTERNATIVE_BASE_VARIANT] = Modifications(modification_list)  # type: ignore

                if not lookups:
                    continue

                raise KeyError(f"After {lookup}, must be Empty!")

            ## Base
            if lookup.code == waycode[Ways.GOLD_BASE]:

                if not lookups:
                    waypaths.gold_base = Ways.GOLD_BASE
                    continue

                if lookups[0].code == waycode[Ways.GOLD_BASE_VARIANT]:
                    waypaths.gold_base = Ways.GOLD_BASE_VARIANT
                    continue

                raise KeyError(
                    f"After {lookup}, {lookups[-1]} must be either Empty, or a Base Variant."
                )

            ## Base Variant
            if lookup.code == waycode[Ways.GOLD_BASE_VARIANT]:
                if not lookups:
                    raise KeyError(f"Must have at least one modification for {lookup}")

                if lookups[0].plane != "MODIFICATION":
                    raise KeyError(
                        f"next {lookups[0]} must be a modification for {lookup}"
                    )

                while lookups:
                    if lookups[0].plane != "MODIFICATION":
                        break

                    modification_lookup = lookups.pop(0)
                    modification_list.append(
                        Modification(
                            modification_lookup.block,
                            modification_lookup.section,
                            modification_lookup.codename,
                        )
                    )

                modifications[Ways.GOLD_BASE_VARIANT] = Modifications(modification_list)  # type: ignore

                if not lookups:
                    continue

                raise KeyError(f"After {lookup}, must be Empty!")

            raise KeyError(f"Unknown Key {lookup}!")

        return (waypaths, modifications)

    ## pylint error, python 3.11 prob fixes this.
    @staticmethod
    def build_gold_models(  # pylint: disable="inconsistent-return-statements"
        waypaths_mods: WayPathsModificationsT,
    ) -> Gold:
        """Take a WayPaths and Extracted Modifications and Build Gold Models"""
        waypaths: WayPaths = waypaths_mods[0]
        modifications: ParseFilename.ModificationsT = waypaths_mods[1]

        if waypaths.gold == Ways.GOLD:
            return Gold(Ways.GOLD)

        if waypaths.gold == Ways.GOLD_ALTERNATIVE:
            if waypaths.gold_alternative == Ways.GOLD_ALTERNATIVE:
                return Gold(
                    GoldAlternative(
                        modifications[Ways.GOLD_ALTERNATIVE],
                        Ways.GOLD_ALTERNATIVE,
                    )
                )
            if waypaths.gold_alternative == Ways.GOLD_ALTERNATIVE_BASE:
                if waypaths.gold_alternative_base == Ways.GOLD_ALTERNATIVE_BASE:
                    return Gold(
                        GoldAlternative(
                            modifications[Ways.GOLD_ALTERNATIVE],
                            GoldAlternativeBase(Ways.GOLD_ALTERNATIVE_BASE),
                        )
                    )
                if waypaths.gold_alternative_base == Ways.GOLD_ALTERNATIVE_BASE_VARIANT:
                    return Gold(
                        GoldAlternative(
                            modifications[Ways.GOLD_ALTERNATIVE],
                            GoldAlternativeBase(
                                GoldAlternativeBaseVariant(
                                    modifications[Ways.GOLD_ALTERNATIVE_BASE_VARIANT]
                                ),
                            ),
                        )
                    )

        if waypaths.gold == Ways.GOLD_BASE:
            if waypaths.gold_base == Ways.GOLD_BASE:
                return Gold(GoldBase(Ways.GOLD_BASE))
            if waypaths.gold_base == Ways.GOLD_BASE_VARIANT:
                return Gold(
                    GoldBase(GoldBaseVariant(modifications[Ways.GOLD_BASE_VARIANT]))
                )

    @staticmethod
    def parse_filename(  # pylint: disable="too-many-locals"
        all_codes: AllCodes, filename: str
    ) -> Filename:
        """Parse the Filename"""

        # Library Name
        library_name: LibraryName = LibraryName(filename.split("-").pop(0)[:3])

        # Item Number
        item_number: ItemNumber = ItemNumber(
            int(filename.split("-")[0][3:], 16) - 0x100000
        )

        ## Library Entry
        library_entry = LibraryEntry(library_name, item_number)

        data: List[str] = filename.split("-", maxsplit=1)[1].split(".")

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
        data_types: Dict[str, Literal["Index", "Metadata", "Media"]] = {
            "index": "Index",
            "metadata": "Metadata",
            "media": "Media",
        }

        data_type_lookup: NamecodeLookup = lookups.pop(-1)
        if data_type_lookup.plane != "DATATYPE":
            if data_type_lookup.block != "DataType":
                if data_type_lookup.section != "datatype":
                    raise KeyError(data_type_lookup)

        data_type: DataType = DataType(data_types[data_type_lookup.codename])

        gold: Gold = ParseFilename.build_gold_models(
            ParseFilename.find_path_and_extract_modifications(all_codes, lookups)
        )

        return Filename(
            library_entry,
            listing,
            gold,
            data_type,
            extention,
        )


class ParseFilenameTest:  # pylint: disable=too-few-public-methods
    """Filename to model."""


if __name__ == "__main__":
    pass
