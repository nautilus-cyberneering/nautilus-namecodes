"""Data Classes for Constructed Namecodes"""

from dataclasses import dataclass, field


@dataclass
class SectionCodes:
    """Data Class for Generated Section Codes"""

    name: str
    codepoints_allocated: range
    codes: dict[int, str]

    def gen_output_range(self) -> str:
        """Generate Pretty Output For Codepoints Allocated Range"""
        return (
            f"0x{self.codepoints_allocated.start:=03X}"
            f" - "
            f"0x{self.codepoints_allocated.stop:=03X}"
        )


@dataclass
class BlockCodes(SectionCodes):
    """Data Class for Generated Block Codes"""

    sections: list[SectionCodes]
    codes: dict[int, str] = field(init=False)

    def __post_init__(self) -> None:
        self.codes = {}
        for section in self.sections:
            self.codes |= section.codes


@dataclass
class PlaneCodes(SectionCodes):
    """Data Class for Generated Plane Codes"""

    blocks: list[BlockCodes]
    codes: dict[int, str] = field(init=False)

    def __post_init__(self) -> None:
        self.codes = {}
        for block in self.blocks:
            self.codes |= block.codes


@dataclass
class AllCodes(SectionCodes):
    """Data Class for all the Generated Namecodes"""

    planes: list[PlaneCodes]
    codes: dict[int, str] = field(init=False)
    scheme_version: str

    def __post_init__(self) -> None:
        self.codes = {}
        for plane in self.planes:
            self.codes |= plane.codes
