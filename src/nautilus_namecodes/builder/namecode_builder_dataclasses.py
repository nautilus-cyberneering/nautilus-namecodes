"""Data Classes used to build Namecodes"""

from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass
from itertools import accumulate

from nautilus_namecodes.namecodes_dataclasses import (
    BlockCodes,
    PlaneCodes,
    SectionCodes,
)


@dataclass(frozen=True)
class ConstantValues:
    """Values that are constant over the entire generation process."""

    page_size: int = 0x010


@dataclass
class CommonValues:
    """Attributes that are common all generation data classes."""

    name: str


class CommonMethods(ABC):  # pylint: disable=too-few-public-methods
    """Methods that are common to all generation data classes."""

    @abstractmethod
    def get_pages_allocated(self) -> int:
        """Return the number of allocated pages."""


@dataclass
class Section(CommonValues, CommonMethods):
    """Values over one or more page"""

    values: list[str]
    name_value_format: str = "({name}) {value}"

    def get_pages_allocated(self) -> int:
        _number_of_items: int = len(self.values)

        _full_pages: int = _number_of_items // ConstantValues.page_size
        _partial_page: bool = bool(_number_of_items % ConstantValues.page_size)

        _pages_used = _full_pages + (0, 1)[_partial_page]
        _pages_allocated = (1, _pages_used)[
            bool(_pages_used)
        ]  # always have a page allocated

        return _pages_allocated

    def get_section_codes(self, starting_codepoint: int, /) -> SectionCodes:
        """Generate codes and return the filled SectionsCode Data Class"""

        _codepoints_allocated: range = range(
            starting_codepoint,
            starting_codepoint
            + self.get_pages_allocated() * ConstantValues.page_size
            - 1,
        )

        _used_codepoints: range = range(
            starting_codepoint, starting_codepoint + len(self.values)
        )

        _values_formated: list[str] = [
            self.name_value_format.format(name=self.name, value=value)
            for value in self.values
        ]

        _codes: dict[int, str] = dict(zip(_used_codepoints, _values_formated))

        return SectionCodes(
            name=self.name, codepoints_allocated=_codepoints_allocated, codes=_codes
        )

    @staticmethod
    def generate_pages_of_values(
        *, base_name: str, pages_to_use: int, gen_format: str
    ) -> list[str]:

        """Static: Generate a full page of values from given format."""
        values: list[str] = [
            gen_format.format(name=base_name, value=value)
            for value in range(1, pages_to_use * ConstantValues.page_size)
        ]
        return values


@dataclass
class Block(CommonValues, CommonMethods):
    """A Group of Sections"""

    sections: list[Section]
    pages_minimum: InitVar[int] = 0

    def __post_init__(self, pages_minimum: int) -> None:
        self.__pages_minimum = pages_minimum

    def get_page_allocations(self) -> list[int]:
        """Get the number of allocated pages per Section"""

        return [section.get_pages_allocated() for section in self.sections]

    def get_pages_allocated(self) -> int:
        _pages_used: int = sum(self.get_page_allocations())
        _pages_min: int = self.__pages_minimum
        return (_pages_used, _pages_min)[_pages_used < _pages_min]

    def get_block_codes(self, starting_codepoint: int, /) -> BlockCodes:
        """Generate codes and return the filled BlockCodes Data Class"""

        _section_offsets: list[int] = list(
            accumulate([0] + self.get_page_allocations())
        )

        _sections_and_offsets: list[tuple[Section, int]] = list(
            zip(self.sections, _section_offsets)
        )

        _section_codes: list[SectionCodes] = [
            section_and_offset[0].get_section_codes(
                starting_codepoint + section_and_offset[1] * ConstantValues.page_size
            )
            for section_and_offset in _sections_and_offsets
        ]

        _codepoints_allocated = range(
            starting_codepoint,
            starting_codepoint
            + self.get_pages_allocated() * ConstantValues.page_size
            - 1,
        )

        _block_codes: BlockCodes = BlockCodes(  # pylint: disable=no-value-for-parameter
            name=self.name,
            codepoints_allocated=_codepoints_allocated,
            sections=_section_codes,
        )

        return _block_codes


@dataclass
class Plane(CommonValues, CommonMethods):
    """A Logical Plane"""

    blocks: list[Block]

    def get_block_page_allocations(self) -> list[int]:
        """Get the number of allocated pages per Block"""

        return [block.get_pages_allocated() for block in self.blocks]

    def get_pages_allocated(self) -> int:
        return sum(self.get_block_page_allocations())

    def get_plane_codes(self, starting_codepoint: int, /) -> PlaneCodes:
        """Generate codes and return the filled PlaneCodes Data Class"""

        _block_offsets: list[int] = list(
            accumulate([0] + self.get_block_page_allocations())
        )
        # print(_section_starting_pages)

        _blocks_and_offsets: list[tuple[Block, int]] = list(
            zip(self.blocks, _block_offsets)
        )

        _block_codes: list[BlockCodes] = [
            block_and_offset[0].get_block_codes(
                starting_codepoint + block_and_offset[1] * ConstantValues.page_size
            )
            for block_and_offset in _blocks_and_offsets
        ]

        _codepoints_allocated = range(
            starting_codepoint,
            starting_codepoint
            + self.get_pages_allocated() * ConstantValues.page_size
            - 1,
        )

        _plane_codes: PlaneCodes = PlaneCodes(  # pylint: disable=no-value-for-parameter
            name=self.name,
            codepoints_allocated=_codepoints_allocated,
            blocks=_block_codes,
        )

        return _plane_codes
