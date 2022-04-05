"""Dataclasses for the Data Encoded into a Namecode Filename"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import re

# from pydantic.dataclasses import dataclass
from typing import Deque, List, Literal, Optional, Tuple, Union

import pydantic


from nautilus_namecodes.namecodes_dataclasses import AllCodes


class Codes(ABC):
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

    def get_formated_entry_string(self) -> str:
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


class Way(Codes, ABC):
    """Abstract Way Class"""

    way: Optional[str] = None

    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        """Looks up the way from codes from the all_codes data structure."""

        if isinstance(self.way, str):
            return all_codes.planes["WAY"].blocks["Way"].sections["way"].codes[self.way]

        raise TypeError('Vairabe "way" is not a string.')

    @abstractmethod
    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        """Recursively get all the codes in order."""


### Hack for Pydantic
### We use this Modifications class as a temporay construct.
### After https://github.com/samuelcolvin/pydantic/issues/3675 we will use a recursive modification model.


@pydantic.dataclasses.dataclass
class Modifications(Codes):
    """A list of modifications along the way an artwork in the Library."""

    modifications: List[Modification]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        """Looks Up and returns the codes from the Namecodes Database"""

        codes: List[Tuple[int, str]] = []

        for modification in self.modifications:
            for code in modification.get_codes(all_codes):
                codes.append(code)

        return codes


@dataclass
class DataType(Codes):
    """The Type used in the Library"""

    basic_type: Union[Literal["index"], Literal["metadata"], Literal["media"]]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [
            all_codes.planes["DATATYPE"]
            .blocks["DataType"]
            .sections["datatype"]
            .codes[f"{self.basic_type}"]
        ]


@dataclass
class BaseVariant(Way):
    """Modified Base from Unmodified Gold"""

    way = "variant"

    modifications: Modifications

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [*self.modifications.get_codes(all_codes), self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return self.get_codes(all_codes)


@dataclass
class Base(Way):
    """Unmodified Base from Unmodified Gold"""

    way = "base"

    base_or_vairant: Union[Literal["base"], BaseVariant]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        if isinstance(self.base_or_vairant, BaseVariant):
            return [
                *self.base_or_vairant.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        return self.get_codes(all_codes)


@dataclass
class BaseAlternativeVairant(Way):
    """ "Modified Base from Alternative Gold"""

    way = "variant"

    modifications: Modifications

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [*self.modifications.get_codes(all_codes), self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return self.get_codes(all_codes)


@dataclass
class BaseAlternative(Way):
    """Unmodified Base from Alternative Gold"""

    way = "base"

    base_alternative_or_vairant: Union[
        Literal["base-alternative"], BaseAlternativeVairant
    ]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        if isinstance(self.base_alternative_or_vairant, BaseAlternativeVairant):
            return [
                *self.base_alternative_or_vairant.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        return self.get_codes(all_codes)


@dataclass
class GoldAlternative(Way):
    """Alternative Gold"""

    way = "alternative"

    modifications: Modifications
    gold_or_base_alternative: Union[Literal["alternative"], BaseAlternative]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [*self.modifications.get_codes(all_codes), self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        if isinstance(self.gold_or_base_alternative, BaseAlternative):
            return [
                *self.gold_or_base_alternative.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        return self.get_codes(all_codes)


@dataclass
class Gold(Way):
    """Unmodified Gold"""

    way = "gold"

    gold_or_alternative_or_base: Union[Literal["gold"], GoldAlternative, Base]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        return [self.get_way(all_codes)]

    def get_codes_r(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        if isinstance(self.gold_or_alternative_or_base, GoldAlternative):
            return [
                *self.gold_or_alternative_or_base.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        if isinstance(self.gold_or_alternative_or_base, Base):
            return [
                *self.gold_or_alternative_or_base.get_codes_r(all_codes),
                *self.get_codes(all_codes),
            ]
        return self.get_codes(all_codes)


@dataclass
class Extention:
    """Filename Extention"""

    extention: str = pydantic.Field(
        None,
        title="File Extention",
        min_length=1,
        regex=r"\A[^\s\t\n\r\f\v\b\0\\\/\"\<\>\|\:\*\?]+\Z",
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
    type: DataType
    extention: Extention

    def get_filename(self, all_codes: AllCodes) -> str:
        """Return the encoded filename."""

        listing_codes = self.listing.get_codes(all_codes)
        modification_codes = self.gold.get_codes_r(all_codes)
        type_code = self.type.get_codes(all_codes)

        return (
            f"{self.library_entry.get_formated_entry_string()}"
            "-"
            f"{'.'.join(map(str,list(zip(*listing_codes))[0]))}"
            "."
            f"{'.'.join(map(str,list(zip(*modification_codes))[0]))}"
            "."
            f"{'.'.join(map(str,list(zip(*type_code))[0]))}"
            "."
            f"{self.extention.get_string()}"
        )
