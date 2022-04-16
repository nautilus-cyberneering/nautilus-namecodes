"""Dataclasses for the Data Encoded into a Namecode Filename"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import reduce

# from pydantic.dataclasses import dataclass
from typing import (  # pylint: disable="unused-import"
    List,
    Literal,
    Mapping,
    Set,
    Tuple,
    Union,
)

import pydantic

from nautilus_namecodes.namecodes_dataclasses import AllCodes


class Codes(ABC):  # pylint: disable="too-few-public-methods"
    """Abstract Codes Class"""

    @abstractmethod
    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        """Used to form the list of Namecodes"""


@dataclass
class LibraryName:
    """A Short String that Identifies the Library"""

    library_code: str = pydantic.Field(
        None,
        title="Global Library Code",
        description="Three letter code, all lowercase or all uppercase.",
        min_length=3,
        max_length=3,
        regex=r"^[a-z]{3}|[A-Z]{3}\Z",
    )


@dataclass
class ItemNumber:
    """The Funderemental Reference for a Conceptual Artwork in the Library"""

    item_number: int = pydantic.Field(
        None, title="Item Number in Library", ge=0x0000, lt=0xFFFE
    )


@dataclass
class LibraryEntry:
    """The Library and Item Number Dataclass"""

    library: LibraryName
    item: ItemNumber

    def get_formatted_entry_string(self) -> str:
        """Get Formatted output for filename."""
        return f"{self.library.library_code}{self.item.item_number + 0x100000:=X}"


@dataclass
class Listing(Codes):
    """Listing Reference"""

    edition: int
    revision: int

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        edition_code: Tuple[int, str] = (
            all_codes.planes["LISTING"]
            .blocks["Edition"]
            .sections["edition"]
            .codes[f"edition: #{self.edition}"]
        )

        revision_code: Tuple[int, str] = (
            all_codes.planes["LISTING"]
            .blocks["Revision"]
            .sections["revision"]
            .codes[f"revision: #{self.revision}"]
        )

        return [edition_code, revision_code]


@dataclass
class Modification(Codes):
    """Basic Reference for a Modification"""

    block: str
    section: str
    code: str

    # pydantic bug: https://github.com/samuelcolvin/pydantic/issues/3675

    # modification: Optional[Modification] = None

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        """Looks Up and returns the codes from the Namecodes Database"""

        codes: List[Tuple[int, str]] = []

        code: Tuple[int, str] = (
            all_codes.planes["MODIFICATION"]
            .blocks[self.block]
            .sections[self.section]
            .codes[self.code]
        )

        codes.append(code)

        # pydantic bug: https://github.com/samuelcolvin/pydantic/issues/3675

        # if isinstance(self.modification, Modification):
        #     for code in self.modification.get_codes(all_codes):
        #         codes.append(code)

        return codes


class Ways(Enum):
    """Enum for Ways"""

    GOLD = "Gold"
    GOLD_ALTERNATIVE = "GoldAlternative"
    GOLD_ALTERNATIVE_BASE = "GoldAlternativeBase"
    GOLD_ALTERNATIVE_BASE_VARIANT = "GoldAlternativeBaseVariant"
    GOLD_BASE = "GoldBase"
    GOLD_BASE_VARIANT = "GoldBaseVariant"


class WayPaths:  # pylint: disable="too-few-public-methods"
    """Paths a Way can Take"""

    gold: Literal[Ways.GOLD, Ways.GOLD_ALTERNATIVE, Ways.GOLD_BASE]
    gold_alternative: Literal[Ways.GOLD_ALTERNATIVE, Ways.GOLD_ALTERNATIVE_BASE]
    gold_alternative_base: Literal[
        Ways.GOLD_ALTERNATIVE_BASE, Ways.GOLD_ALTERNATIVE_BASE_VARIANT
    ]
    gold_base: Literal[Ways.GOLD_BASE, Ways.GOLD_BASE_VARIANT]


class Way(Codes, ABC):
    """Abstract Way Class"""

    way: Literal[
        Ways.GOLD,
        Ways.GOLD_ALTERNATIVE,
        Ways.GOLD_ALTERNATIVE_BASE,
        Ways.GOLD_ALTERNATIVE_BASE_VARIANT,
        Ways.GOLD_BASE,
        Ways.GOLD_BASE_VARIANT,
    ]

    @staticmethod
    def snake_case(string: str) -> str:
        """from camel case to snake case (from geeks for geeks)"""

        return reduce(lambda x, y: x + ("_" if y.isupper() else "") + y, string).lower()

    @staticmethod
    def get_way_code(all_codes: AllCodes, way: Ways) -> Tuple[int, str]:
        """Looks up the way from codes from the all_codes data structure."""
        return (
            all_codes.planes["WAY"]
            .blocks["Way"]
            .sections["way"]
            .codes[Way.snake_case(way.value)]
        )

    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        """Get way code from current class."""
        return Way.get_way_code(all_codes, self.way)

    @abstractmethod
    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        """Recursively get all the codes in order."""


### Hack for Pydantic
### We use this Modifications class as a temporary construct.
### After https://github.com/samuelcolvin/pydantic/issues/3675 we will use a recursive modification model.


@pydantic.dataclasses.dataclass  # pylint: disable=c-extension-no-member
class Modifications(Codes):
    """A unique list of modifications along the way an artwork in the Library."""

    modifications: List[Modification]

    def __post_init_post_parse__(self) -> None:
        """Used to detect and raise and error for the first (if any) duplicates in the modification list"""
        modification_set: Set[str] = set([])
        for modification in self.modifications:
            set_size: int = len(modification_set)
            modification_set.add(
                f"{modification.block}{modification.section}{modification.code}"
            )

            if len(modification_set) == set_size:
                raise ValueError(
                    f"Duplicate found in Modifications List:{modification}"
                )

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        """Looks Up and returns the codes from the Namecodes Database"""

        codes: List[Tuple[int, str]] = []

        for modification in self.modifications:
            for code in modification.get_codes(all_codes):
                codes.append(code)

        return codes


def mk_modifications(modifications: List[Modification]) -> Modifications:
    """Mypy helper class function"""
    return Modifications(modifications)  # type: ignore


@dataclass
class DataType(Codes):
    """The Type used in the Library"""

    basic_type: Literal["Index", "Metadata", "Media"]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [
            all_codes.planes["DATATYPE"]
            .blocks["DataType"]
            .sections["datatype"]
            .codes[f"{self.basic_type.lower()}"]
        ]


@dataclass
class GoldBaseVariant(Way):
    """Modified Base from Unmodified Gold"""

    way = Ways.GOLD_BASE_VARIANT

    modifications: Modifications

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [*self.modifications.get_codes(all_codes), self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return self.get_codes(all_codes)


@dataclass
class GoldBase(Way):
    """Unmodified Base from Unmodified Gold"""

    way = Ways.GOLD_BASE

    base_or_base_variant: Union[Literal[Ways.GOLD_BASE], GoldBaseVariant]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        if isinstance(self.base_or_base_variant, GoldBaseVariant):
            return [
                *self.base_or_base_variant.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        return self.get_codes(all_codes)


@dataclass
class GoldAlternativeBaseVariant(Way):
    """ "Modified Base from Alternative Gold"""

    way = Ways.GOLD_ALTERNATIVE_BASE_VARIANT

    modifications: Modifications

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [*self.modifications.get_codes(all_codes), self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return self.get_codes(all_codes)


@dataclass
class GoldAlternativeBase(Way):
    """Unmodified Base from Alternative Gold"""

    way = Ways.GOLD_ALTERNATIVE_BASE

    base_or_base_variant: Union[
        Literal[Ways.GOLD_ALTERNATIVE_BASE], GoldAlternativeBaseVariant
    ]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        if isinstance(self.base_or_base_variant, GoldAlternativeBaseVariant):
            return [
                *self.base_or_base_variant.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        return self.get_codes(all_codes)


@dataclass
class GoldAlternative(Way):
    """Alternative Gold"""

    way = Ways.GOLD_ALTERNATIVE

    modifications: Modifications

    alternative_or_alternative_base: Union[
        Literal[Ways.GOLD_ALTERNATIVE], GoldAlternativeBase
    ]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [*self.modifications.get_codes(all_codes), self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        if isinstance(self.alternative_or_alternative_base, GoldAlternativeBase):
            return [
                *self.alternative_or_alternative_base.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        return self.get_codes(all_codes)


@dataclass
class Gold(Way):
    """Unmodified Gold"""

    way = Ways.GOLD

    gold_or_gold_alternative_or_gold_base: Union[
        Literal[Ways.GOLD], GoldAlternative, GoldBase
    ]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        if isinstance(self.gold_or_gold_alternative_or_gold_base, GoldAlternative):
            return [
                *self.gold_or_gold_alternative_or_gold_base.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        if isinstance(self.gold_or_gold_alternative_or_gold_base, GoldBase):
            return [
                *self.gold_or_gold_alternative_or_gold_base.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        return self.get_codes(all_codes)


@dataclass
class Extension:
    """Filename Extension"""

    # note, not not accept extension just a single period
    extention: str = pydantic.Field(
        None,
        title="File Extension",
        description=(
            "Any unicode character, except for: control characters,"
            "null, slashes, pipe, whitespace, double periods, asterisk, question mark, and dash."
        ),
        min_length=1,
        regex=r"(?u)\A(?:(?!\.{2,})[^\s\t\n\r\f\v\b\0\\\/\"\<\>\|\:\*\?\-])*\Z",
    )

    def get_string(self) -> str:
        """Simple String Getter"""
        return self.extention


@dataclass
class Filename:
    """The Data that is encoded into a Filename."""

    library_entry: LibraryEntry
    listing: Listing
    gold: Gold
    data_type: DataType
    extension: Extension

    def get_filename(self, all_codes: AllCodes) -> str:
        """Return the encoded filename."""

        listing_codes = self.listing.get_codes(all_codes)
        modification_codes = self.gold.get_codes_r(all_codes)
        type_code = self.data_type.get_codes(all_codes)

        return (
            f"{self.library_entry.get_formatted_entry_string()}"
            "-"
            f"{'.'.join(map(str,list(zip(*listing_codes))[0]))}"
            "."
            f"{'.'.join(map(str,list(zip(*modification_codes))[0]))}"
            "."
            f"{'.'.join(map(str,list(zip(*type_code))[0]))}"
            "."
            f"{self.extension.get_string()}"
        )
