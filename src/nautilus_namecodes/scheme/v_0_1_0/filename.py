"""Dataclass for the Data Encoded into a Namecode Filename"""

from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class LibraryCode:
    library_code: str


@dataclass
class ItemCode:
    item_code: int


@dataclass
class Listing:
    edition: int
    revision: int


@dataclass
class BaseVairant:
    literal: Literal["modified"]
    modifications: List[int]


@dataclass
class Base:
    literal: Literal["clean"]
    base_vairant: Optional[BaseVairant] = None


@dataclass
class BaseAlternativeVairant:
    literal: Literal["modified"]
    modifications: List[int]


@dataclass
class BaseAlternative:
    literal: Literal["clean"]
    base_alternative_vairant: Optional[BaseAlternativeVairant] = None


@dataclass
class GoldAlternative:
    literal: Literal["alternative"]
    modifications: List[int]
    base_alternative: Optional[BaseAlternative] = None


@dataclass
class Gold:
    literal: Literal["original"]
    alternative: Optional[GoldAlternative] = None
    base: Optional[Base] = None


@dataclass
class Filename:
    library: LibraryCode
    item: ItemCode
    listing: Listing
    info: Gold
