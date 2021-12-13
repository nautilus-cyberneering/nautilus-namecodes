"""Generate Namecodes from Values"""

from typing import List

from nautilus_namecodes.namecodes_dataclasses import (
    AllCodes,
    BlockBranch,
    BlockCodes,
    PlaneBranch,
    PlaneCodes,
    Range,
    SectionCodes,
    SectionStub,
    TreeStub,
)
from nautilus_namecodes.scheme.v_0_1_0.namecode_values import (
    BasicType,
    Modifications,
    Purpose,
)

__scheme_version__ = "v.0.1.0"


class BaseNameCodes(BasicType):
    """Generate the Plane Codes for the BasicType"""

    def __init__(self) -> None:
        super().__init__()

        self._start: int = 0x000
        self._planecodes: PlaneCodes = self.get_plane.get_plane_codes(self._start)

    @property
    def get_plane_codes(self) -> PlaneCodes:
        """Returns the Plane Codes Property"""
        return self._planecodes


class PurposeNameCodes(Purpose):
    """Generate the Plane Codes for the Purpose"""

    def __init__(self) -> None:
        super().__init__()

        self._start: int = 0x030
        self._planecodes: PlaneCodes = self.get_plane.get_plane_codes(self._start)

    @property
    def get_plane_codes(self) -> PlaneCodes:
        """Returns the Plane Codes Property"""
        return self._planecodes


class ModificationsNameCodes(Modifications):
    """Generate the Plane Codes for the Modifications"""

    def __init__(self) -> None:
        super().__init__()

        self._start: int = 0x600
        self._planecodes: PlaneCodes = self.get_plane().get_plane_codes(self._start)

    @property
    def get_plane_codes(self) -> PlaneCodes:
        """Returns the Plane Codes Property"""
        return self._planecodes


class AllNameCodes:
    """Group Together All Namecodes"""

    def __init__(self) -> None:
        self._name: str = "Nautilus Namecodes"

        self._planecodes: list[PlaneCodes] = list(
            [
                BaseNameCodes().get_plane_codes,
                PurposeNameCodes().get_plane_codes,
                ModificationsNameCodes().get_plane_codes,
            ]
        )

        self._planecodes.sort(
            key=lambda planecode: planecode.codepoints_allocated.start
        )

        self._allcodes: AllCodes = AllCodes(  # pylint: disable=no-value-for-parameter
            name=self._name,
            description=__doc__,
            codepoints_allocated=self.get_codepoints_allocated(),
            planes=self._planecodes,
            scheme_version=__scheme_version__,
        )

    @property
    def get_all_codes(self) -> AllCodes:
        """Get All the NameCodes"""
        return self._allcodes

    def get_all_codepoints_allocated(self) -> list[Range]:
        """Get List of Codepoints Allocated"""
        return [planecode.codepoints_allocated for planecode in self._planecodes]

    def get_codepoints_allocated(self) -> Range:
        """Get the Full Range of Namecode Codepoints"""
        _planecode_codepoints: list[Range] = self.get_all_codepoints_allocated()

        return Range.mk_range(
            range(
                _planecode_codepoints[0].start,
                _planecode_codepoints[-1].stop,
            )
        )


class TreeStubGen:  # pylint: disable="too-few-public-methods"
    """Fill the Stub Tree Dataclass"""

    def __init__(self) -> None:
        _all_name_codes: AllCodes = AllNameCodes().get_all_codes

        _plane_branches: List[PlaneBranch] = []

        plane: PlaneCodes
        for plane in _all_name_codes.planes:

            _block_branches: List[BlockBranch] = []
            block: BlockCodes
            for block in plane.blocks:

                _section_stubs: List[SectionStub] = []
                section: SectionCodes
                for section in block.sections:
                    _section_stubs.append(
                        SectionStub(
                            name=section.name,
                            description=section.description,
                            codepoints_allocated=section.codepoints_allocated,
                        )
                    )

                _block_branches.append(
                    BlockBranch(
                        name=block.name,
                        description=block.description,
                        codepoints_allocated=block.codepoints_allocated,
                        section_stubs=_section_stubs,
                    )
                )

            _plane_branches.append(
                PlaneBranch(
                    plane.name,
                    description=plane.description,
                    codepoints_allocated=plane.codepoints_allocated,
                    block_branches=_block_branches,
                )
            )

        self._tree_stub: TreeStub = TreeStub(
            _all_name_codes.name,
            description=_all_name_codes.name,
            codepoints_allocated=_all_name_codes.codepoints_allocated,
            plane_branches=_plane_branches,
            scheme_version=_all_name_codes.scheme_version,
        )

    @property
    def tree_stub(self) -> TreeStub:
        """Get All the NameCodes"""
        return self._tree_stub
