"""Namecodes Specification"""

# pylint: disable=too-few-public-methods

from nautilus_namecodes.builder.namecode_builder_dataclasses import (
    Block,
    Plane,
    Section,
)


class BasicType:
    """Basic Types of Namecodes: Index, Metadata, and Media"""

    _name: str = "BasicType"
    _values: list[str] = ["index", "metadata", "media"]

    _sections: list[Section] = list([Section(name=_name.lower(), values=_values)])

    def __init__(self) -> None:
        self._blocks: list[Block] = list(
            [Block(name=BasicType._name, sections=BasicType._sections)]
        )
        self._plane: Plane = Plane(name=BasicType._name.upper(), blocks=self._blocks)

    @property
    def get_blocks(self) -> list[Block]:
        """Return a list of Block Data Classes"""
        return self._blocks

    @property
    def get_plane(self) -> Plane:
        """Returns the Plane Data Class"""
        return self._plane


class Purpose:
    """The Basic Purpose of Media File"""

    _name: str = "Purpose"

    class Purposes:
        """The Purposes connected to a Media File"""

        _name: str = "Purposes"

        _names: list[str] = ["gold", "alternative", "base", "variant"]

        sections: list[Section] = [
            Section(name=section_name.lower(), values=["index", "metadata", "media"])
            for section_name in _names
        ]

        block: Block = Block(name=_name, sections=sections)

    def __init__(self) -> None:
        self._blocks: list[Block] = list([Purpose.Purposes.block])
        self._plane: Plane = Plane(name=Purpose._name.upper(), blocks=self._blocks)

    @property
    def get_blocks(self) -> list[Block]:
        """Return a list of Block Data Classes"""
        return self._blocks

    @property
    def get_plane(self) -> Plane:
        """Returns the Plane Data Class"""
        return self._plane


class Modifications:
    """The Modifications Listed for a Media File"""

    _name: str = "Modification"

    class Editions:
        """Media Files may have Many Editions"""

        _name: str = "Edition"
        _values: list[str] = Section.generate_pages_of_values(
            base_name=_name.lower(), pages_to_use=0x010, gen_format="{name}: #{value}"
        )

        sections: list[Section] = list([Section(name=_name.lower(), values=_values)])
        block: Block = Block(name=_name, sections=sections)

    class Revisions:
        """Media Files May be Revised many times"""

        _name: str = "Revision"
        _values: list[str] = Section.generate_pages_of_values(
            base_name=_name.lower(), pages_to_use=0x010, gen_format="{name}: #{value}"
        )

        sections: list[Section] = list([Section(name=_name.lower(), values=_values)])
        block: Block = Block(name=_name, sections=sections)

    class Adaptions:
        """Media Files may be adapted"""

        _name: str = "Adaption"

        sections: list[Section] = [
            Section(name="*reserved*", values=[]),
            Section(
                name="focus",
                values=[
                    "background",
                    "background blur",
                    "background transparent",
                    "foreground",
                    "foreground blur",
                    "foreground transparent",
                    "wash",
                ],
            ),
            Section(
                name="style",
                values=["cartoon", "outline", "line-art", "charcoal"],
            ),
            Section(
                name="prospective",
                values=[
                    "tall",
                    "wide",
                    "prospective",
                    "wide-angle",
                    "macro",
                    "top",
                    "bottom",
                    "left",
                    "right",
                    "inside",
                    "outside",
                ],
            ),
            Section(
                name="context",
                values=["day", "night", "windy", "hot", "underwater"],
            ),
            Section(
                name="action",
                values=["sleeping", "running", "eating", "dancing"],
            ),
            Section(
                name="edit",
                values=[
                    "loud",
                    "quite",
                    "looping",
                    "dynamic",
                    "soft",
                    "aggressive",
                ],
            ),
        ]

        block: Block = Block(name=_name, sections=sections)

    class Transformations:
        """Media Files may be transformed"""

        _name: str = "Transformation"
        sections: list[Section] = [
            Section(name="*reserved*", values=[]),
            Section(name="contrast", values=["low", "medium", "high", "extreme"]),
            Section(
                name="colour",
                values=["back and white", "greyscale", "dull", "vivid", "invert"],
            ),
            Section(
                name="aspect",
                values=[
                    "flip vertically",
                    "flip horizontally",
                    "rotate left 90",
                    "rotate right 90",
                    "double height",
                    "double width",
                ],
            ),
            Section(
                name="size",
                values=[
                    ">=512MP",
                    "<512MP",
                    "<50MP",
                    "<12MP",
                    "<10MP",
                    "<8MP",
                    "<6MP",
                    "<5MP",
                    "<4MP",
                    "<3MP",
                    "<2MP",
                    "<1MP",
                    "<0.9MP",
                    "<0.8MP",
                    "<0.7MP",
                    "<0.6MP",
                    "<0.5MP",
                    "<0.4MP",
                    "<0.3MP",
                    "<0.25MP",
                    "<0.2MP",
                    "<0.18MP",
                    "<0.16MP",
                    "<0.15MP",
                    "<0.14MP",
                    "<0.13MP",
                    "<0.12MP",
                    "<0.11MP",
                    "<0.10MP",
                    "<0.09MP",
                    "<0.08MP",
                    "<0.07MP",
                    "<0.06MP",
                    "<0.05MP",
                    "<0.04MP",
                    "<0.03MP",
                    "<0.02MP",
                    "<0.01MP",
                    "<0.009MP",
                    "<0.008MP",
                    "<0.007MP",
                    "<0.006MP",
                    "<0.005MP",
                    "<0.004MP",
                    "<0.003MP",
                    "<0.002MP",
                    "<0.001MP",
                ],
            ),
        ]

        block: Block = Block(name=_name, sections=sections)

    class Formats:
        """Media Files may formatted in various ways"""

        _name: str = "Format"
        sections: list[Section] = [
            Section(name="*reserved*", values=[]),
            Section(name="image_format", values=["tiff", "jpeg", "png"]),
            Section(name="colour_space", values=["sRGB", "AdobeRGB", "P3"]),
            Section(
                name="channel_depth",
                values=[
                    "8bit",
                    "10bit",
                    "12bit",
                    "14bit",
                    "16bit",
                    "24bit",
                    "32bit",
                    "48bit",
                    "64bit",
                ],
            ),
            Section(
                name="compress",
                values=[
                    "uncompressed",
                    "lossless",
                    "transparent",
                    "excellent",
                    "great",
                    "very good",
                    "good",
                    "fair",
                    "poor",
                    "very poor",
                    "worst",
                ],
            ),
        ]

        block: Block = Block(name=_name, sections=sections)

    class Embeddedings:
        """Metadata may be embedded within the media file"""

        _name: str = "Embedded"

        sections: list[Section] = [
            Section(
                name="embedded",
                values=[
                    "unmodified",
                    "blank",
                    "copyright only",
                    "copyright and artist",
                    "full",
                ],
            )
        ]

        block: Block = Block(name=_name, sections=sections)

    def __init__(self) -> None:
        self._blocks: list[Block] = list(
            [
                Modifications.Editions.block,
                Modifications.Revisions.block,
                Modifications.Adaptions.block,
                Modifications.Transformations.block,
                Modifications.Formats.block,
                Modifications.Embeddedings.block,
            ]
        )
        self._plane: Plane = Plane(
            name=Modifications._name.upper(), blocks=self._blocks
        )

    @property
    def get_blocks(self) -> list[Block]:
        """Return a list of Block Data Classes"""
        return self._blocks

    @property
    def get_plane(self) -> Plane:
        """Returns the Plane Data Class"""
        return self._plane
