"""Dataclasses for the Data Encoded into a Namecode Filename"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

# from pydantic.dataclasses import dataclass
from typing import List, Literal, Tuple, Union

import pydantic


from nautilus_namecodes.namecodes_dataclasses import AllCodes


@dataclass
class LibraryCode:
    """A Short String that Identifies the Library"""

    library_code: str


@dataclass
class ItemCode:
    """The Funderemental Reference for a Conceptual Artwork in the Library"""

    item_code: int


@dataclass
class Listing:
    """Basic Listing Reference"""

    edition: int
    revision: int


@dataclass
class Modification:
    """Basic Reference for a Modification"""

    block: str
    section: str
    code: str


### Hack for Pydantic.
@pydantic.dataclasses.dataclass
class Modifications:
    """A list of modifications along the way an artwork in the Library."""

    modifications: List[Modification]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:
        """Looks Up and returns the codes from the Namecodes Database"""

        codes: List[Tuple[int, str]] = []

        for modification in self.modifications:
            code: Tuple[int, str] = (
                all_codes.planes["Modifications"]
                .blocks[modification.block]
                .sections[modification.section]
                .codes[modification.code]
            )

            codes.append(code)

        return codes


@dataclass
class DataType:
    """The Type used in the Library"""

    basic_type: Union[Literal["index"], Literal["metadata"], Literal["media"]]


class Way(ABC):
    """Abstract Way Class"""

    @abstractmethod
    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        """Used to form the list of Namecodes"""


@dataclass
class BaseVariant(Way):
    """Way: Variant"""

    modifications: Modifications

    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        return all_codes.planes["Way"].blocks["Way"].sections["way"].codes["variant"]

    def get_codes(self, all_codes: AllCodes) -> List[Tuple[int, str]]:

        way: Tuple[int, str] = self.get_way(all_codes)

        codes: List[Tuple[int, str]] = self.modifications.get_codes(all_codes)

        return [way, *codes]


@dataclass
class Base(Way):
    """Way: Base"""

    base_or_vairant: Union[Literal["base"], BaseVariant]

    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        pass


@dataclass
class BaseAlternativeVairant(Way):
    """Way: Variant"""

    modifications: Modifications

    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        pass


@dataclass
class BaseAlternative(Way):
    """Way: Base"""

    base_alternative_or_vairant: Union[Literal["base"], BaseAlternativeVairant]

    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        pass


@dataclass
class GoldAlternative(Way):
    """Way: Alternative"""

    modifications: Modifications
    gold_or_base_alternative: Union[Literal["alternative"], BaseAlternative]

    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        pass


@dataclass
class Gold(Way):
    """Way: Gold"""

    gold_alternative_or_base: Union[Literal["gold"], GoldAlternative, Base]

    def get_way(self, all_codes: AllCodes) -> Tuple[int, str]:
        pass


@dataclass
class Filename:
    """The Data that is encoded into a Filename."""

    library: LibraryCode
    item: ItemCode
    listing: Listing
    gold: Gold
    type: DataType
