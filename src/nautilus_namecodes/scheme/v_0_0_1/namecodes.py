"""Generate Namecodes from Values"""


from nautilus_namecodes.namecodes_dataclasses import AllCodes, PlaneCodes
from nautilus_namecodes.scheme.v_0_0_1.namecode_values import (
    BasicType,
    Modifications,
    Purpose,
)

__scheme_version__ = "v.0.0.1"


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
        self._planecodes: PlaneCodes = self.get_plane.get_plane_codes(self._start)

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
            codepoints_allocated=self.get_codepoints_allocated(),
            planes=self._planecodes,
            scheme_version=__scheme_version__,
        )

    @property
    def get_all_codes(self) -> AllCodes:
        """Get All the NameCodes"""
        return self._allcodes

    def get_all_codepoints_allocated(self) -> list[range]:
        """Get List of Codepoints Allocated"""
        return [planecode.codepoints_allocated for planecode in self._planecodes]

    def get_codepoints_allocated(self) -> range:
        """Get the Full Range of Namecode Codepoints"""
        _planecode_codepoints: list[range] = self.get_all_codepoints_allocated()

        return range(_planecode_codepoints[0].start, _planecode_codepoints[-1].stop)
