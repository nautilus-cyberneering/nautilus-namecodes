"""Namecodes Specification"""

# pylint: disable=too-few-public-methods

from typing import Dict, Iterable, List, Tuple

from nautilus_namecodes.builder.namecode_builder_dataclasses import (
    Block,
    Plane,
    Section,
)


class BasicType:
    """Basic Types of Namecodes: Index, Metadata, and Media"""

    _name: str = "BasicType"
    _values: list[str] = ["index", "metadata", "media"]

    @property
    def sections(self) -> Iterable[Section]:
        """Basic Section: index, metadata, and media, types."""
        return list(
            [
                Section(
                    name=self._name.lower(),
                    description=self.__doc__,
                    values=self._values,
                )
            ]
        )

    def __init__(self) -> None:
        self._blocks: list[Block] = list(
            [
                Block(
                    name=self._name,
                    description=self.__doc__,
                    sections=self.sections,
                )
            ]
        )

        self._plane: Plane = Plane(
            name=BasicType._name.upper(),
            description=self.__doc__,
            blocks=self._blocks,
        )

    @property
    def get_blocks(self) -> Iterable[Block]:
        """Returns a Block containing the Basic Section"""
        return self._blocks

    @property
    def get_plane(self) -> Plane:
        """Returns a Plane containing the Basic Block, Section"""
        return self._plane


class Purpose:
    """The Basic Purpose of Media File"""

    _name: str = "Purpose"

    class Purposes:
        """The Purposes connected to a Media File"""

        _name: str = "Purposes"

        _sections: Dict[str, str] = {
            "gold": "Original Processed Artwork from Artists",
            "alternative": "Modified or Transformed version of a Gold Artwork",
            "base": "Processed Artwork for Public Use",
            "variant": "Modified or Transformed Processed Artwork for Public Use",
        }

        _values: List[str] = ["index", "metadata", "media"]

        @property
        def sections(self) -> Iterable[Section]:
            """Returns a list of sections for each purpose type:

            index, metadata, and media types."""

            section_items: Tuple[str, str]
            sections: List[Section] = []

            for section_items in self._sections.items():
                sections.append(
                    Section(
                        name=section_items[0],
                        description=section_items[1],
                        values=self._values,
                    )
                )

            return sections

        @property
        def block(self) -> Block:
            """Returns a newly built Block Class containing the Purpose Sections."""
            return Block(
                name=self._name, description=self.__doc__, sections=self.sections
            )

    def __init__(self) -> None:
        self._blocks: list[Block] = list([Purpose.Purposes().block])
        self._plane: Plane = Plane(
            name=Purpose._name.upper(), description=self.__doc__, blocks=self._blocks
        )

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

        @property
        def sections(self) -> list[Section]:
            """Returns a list of newly built Sections."""
            return list(
                [
                    Section(
                        name=self._name.lower(),
                        description=self.__doc__,
                        values=self._values,
                    )
                ]
            )

        @property
        def block(self) -> Block:
            "Returns a newly built Block Class with name, doc, and sections."
            return Block(
                name=self._name, description=self.__doc__, sections=self.sections
            )

    class Revisions:
        """Media Files May be Revised many times"""

        _name: str = "Revision"
        _values: list[str] = Section.generate_pages_of_values(
            base_name=_name.lower(), pages_to_use=0x010, gen_format="{name}: #{value}"
        )

        @property
        def sections(self) -> list[Section]:
            """Returns a sections containing a list of Revision Numbers (256 numbers)."""
            return list(
                [
                    Section(
                        name=self._name.lower(),
                        description=self.__doc__,
                        values=self._values,
                    )
                ]
            )

        @property
        def block(self) -> Block:
            """Returns the Block containing the Section of Revision Numbers."""
            return Block(
                name=self._name, description=self.__doc__, sections=self.sections
            )

    class Adaptions:
        """Media Files may be adapted"""

        _name: str = "Adaption"

        @property
        def sections(self) -> list[Section]:
            """Returns the a list of Sections detailing how a Media file may be Adapted."""
            return [
                Section(name="*reserved*", description=self.__doc__, values=[]),
                Section(
                    name="focus",
                    description=self.__doc__,
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
                    description=self.__doc__,
                    values=["cartoon", "outline", "line-art", "charcoal"],
                ),
                Section(
                    name="prospective",
                    description=self.__doc__,
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
                    description=self.__doc__,
                    values=["day", "night", "windy", "hot", "underwater"],
                ),
                Section(
                    name="action",
                    description=self.__doc__,
                    values=["sleeping", "running", "eating", "dancing"],
                ),
                Section(
                    name="edit",
                    description=self.__doc__,
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

        @property
        def block(self) -> Block:
            """Returns the Block of Sections detailing how a Media file may be Adapted."""
            return Block(
                name=self._name, description=self.__doc__, sections=self.sections
            )

    class Transformations:
        """Media Files may be transformed"""

        _name: str = "Transformation"

        @property
        def sections(self) -> list[Section]:
            """Returns the list of Sections detailing how a Media file may be Transformed."""
            return [
                Section(name="*reserved*", description=self.__doc__, values=[]),
                Section(
                    name="contrast",
                    description=self.__doc__,
                    values=["low", "medium", "high", "extreme"],
                ),
                Section(
                    name="colour",
                    description=self.__doc__,
                    values=["back and white", "greyscale", "dull", "vivid", "invert"],
                ),
                Section(
                    name="aspect",
                    description=self.__doc__,
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
                    description=self.__doc__,
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

        @property
        def block(self) -> Block:
            """Returns the Block of Sections detailing how a Media file may be Transformed."""
            return Block(
                name=self._name, description=self.__doc__, sections=self.sections
            )

    class Formats:
        """Media Files may formatted in various ways"""

        _name: str = "Format"

        @property
        def sections(self) -> list[Section]:
            """Returns the list of Sections detailing how a Media file may be Formatted."""
            return [
                Section(name="*reserved*", description=self.__doc__, values=[]),
                Section(
                    name="image_format",
                    description=self.__doc__,
                    values=["tiff", "jpeg", "png"],
                ),
                Section(
                    name="colour_space",
                    description=self.__doc__,
                    values=["sRGB", "AdobeRGB", "P3"],
                ),
                Section(
                    name="channel_depth",
                    description=self.__doc__,
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
                    description=self.__doc__,
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

        @property
        def block(self) -> Block:
            """Returns the Block of Sections detailing how a Media file may be Formatted."""
            return Block(
                name=self._name, description=self.__doc__, sections=self.sections
            )

    class Embeddedings:
        """Metadata may be embedded within the media file"""

        _name: str = "Embedded"

        @property
        def sections(self) -> list[Section]:
            """Returns the list of Sections detailing how the media file may have metadata embedded"""
            return [
                Section(
                    name="embedded",
                    description=self.__doc__,
                    values=[
                        "unmodified",
                        "blank",
                        "copyright only",
                        "copyright and artist",
                        "full",
                    ],
                )
            ]

        @property
        def block(self) -> Block:
            """Returns the Block of Sections detailing how the media file may have metadata embedded"""
            return Block(
                name=self._name, description=self.__doc__, sections=self.sections
            )

    def __init__(self) -> None:
        self._blocks: list[Block] = list(
            [
                Modifications.Editions().block,
                Modifications.Revisions().block,
                Modifications.Adaptions().block,
                Modifications.Transformations().block,
                Modifications.Formats().block,
                Modifications.Embeddedings().block,
            ]
        )

        self._plane: Plane = Plane(
            name=Modifications._name.upper(),
            description=self.__doc__,
            blocks=self._blocks,
        )

    def get_blocks(self) -> list[Block]:
        """Return a list of Block Data Classes"""
        return self._blocks

    def get_plane(self) -> Plane:
        """Returns the Plane Data Class"""
        return self._plane
