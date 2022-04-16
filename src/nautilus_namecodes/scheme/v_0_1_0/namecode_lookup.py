"""Simple Dataclass for looking up namecodes from their number"""

from dataclasses import InitVar, dataclass, field
from typing import Tuple

from nautilus_namecodes.namecodes_dataclasses import (
    AllCodes,
    BlockCodes,
    PlaneCodes,
    SectionCodes,
)


@dataclass
class NamecodeLookup:
    """ "A dataclass that allows for looking up of namecodes"""

    all_codes: InitVar[AllCodes]

    namecode: int

    plane: str = field(init=False)
    block: str = field(init=False)
    section: str = field(init=False)
    codename: str = field(init=False)

    code: Tuple[int, str] = field(init=False)

    def __post_init__(self, all_codes: AllCodes):

        plane_codes: PlaneCodes = all_codes.lookup_plane_by_code(self.namecode)
        self.plane = plane_codes.name

        block_codes: BlockCodes = plane_codes.lookup_block_by_code(self.namecode)
        self.block = block_codes.name

        section_codes: SectionCodes = block_codes.lookup_section_by_code(self.namecode)
        self.section = section_codes.name

        code: Tuple[str, Tuple[int, str]] = section_codes.lookup_by_namecode(
            self.namecode
        )
        self.codename = code[0]
        self.code = code[1]
