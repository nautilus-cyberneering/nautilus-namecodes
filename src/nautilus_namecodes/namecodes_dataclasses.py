"""Data Classes for Constructed Namecodes"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type, TypeVar

RangeTypeT = TypeVar("RangeTypeT", bound="Range")


class Range:
    """Placeholder Range Class to help Pydantic."""

    stop: int
    start: int
    step: int = 1

    def __init__(self, stop: int, start: int, step: int) -> None:
        self.stop = stop
        self.start = start
        self.step = step

    @classmethod
    def mk_range(cls: Type[RangeTypeT], _range, /) -> RangeTypeT:
        """Factory to make Range Class from a Standard Range Type"""
        return cls(_range.stop, _range.start, _range.step)

    @property
    def range(self) -> range:
        """Property to get the standard range type."""
        return range(self.start, self.stop, self.step)


@dataclass
class SectionStub:
    """Base Data Class for Sections"""

    name: str
    description: Optional[str]
    codepoints_allocated: Range

    def gen_output_range(self) -> str:
        """Generate Pretty Output For Codepoints Allocated Range"""
        return (
            f"0x{self.codepoints_allocated.start:=03X}"
            f" - "
            f"0x{self.codepoints_allocated.stop:=03X}"
        )


@dataclass
class BlockBranch(SectionStub):
    """Data Class for a Block Branch"""

    section_stubs: List[SectionStub]


@dataclass
class PlaneBranch(SectionStub):
    """Data Class for a Plane Branch"""

    block_branches: List[BlockBranch]


@dataclass
class TreeStub(SectionStub):
    """Data Class for a Stub Tree"""

    plane_branches: List[PlaneBranch]
    scheme_version: str


@dataclass
class SectionCodes(SectionStub):
    """Data Class for Generated Section Codes"""

    codes: Dict[int, str]


@dataclass
class BlockCodes(SectionStub):
    """Data Class for Generated Block Codes"""

    sections: List[SectionCodes]
    codes: Dict[int, str] = field(init=False)

    def __post_init__(self) -> None:
        self.codes = {}
        for section in self.sections:

            # hack for pydantic
            if isinstance(section, Mapping):
                self.codes |= section["codes"]
            else:
                self.codes |= section.codes


@dataclass
class PlaneCodes(SectionStub):
    """Data Class for Generated Plane Codes"""

    blocks: List[BlockCodes]
    codes: Dict[int, str] = field(init=False)

    def __post_init__(self) -> None:
        self.codes = {}
        for block in self.blocks:

            # hack for pydantic
            if isinstance(block, Mapping):
                self.codes |= block["codes"]
            else:
                self.codes |= block.codes


@dataclass
class AllCodes(SectionStub):
    """Data Class for all the Generated Namecodes"""

    planes: List[PlaneCodes]
    codes: Dict[int, str] = field(init=False)
    scheme_version: str

    def __post_init__(self) -> None:
        self.codes = {}
        for plane in self.planes:

            # hack for pydantic
            if isinstance(plane, Mapping):
                self.codes |= plane["codes"]
            else:
                self.codes |= plane.codes
