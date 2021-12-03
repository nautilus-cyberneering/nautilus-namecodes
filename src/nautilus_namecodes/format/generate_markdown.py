"""Format the Generated Namecodes for Markdown Presentation"""

from typing import Iterable, List, Tuple

from snakemd import Document
from snakemd.generator import Element, Header, InlineText, Paragraph, Table

from nautilus_namecodes.namecodes_dataclasses import (
    AllCodes,
    BlockCodes,
    PlaneCodes,
    SectionCodes,
)
from nautilus_namecodes.scheme.v_0_0_1.namecodes import AllNameCodes


class MarkdownOutput:
    """Generate Markdown Formatted Codes."""

    def __init__(self) -> None:
        self.all_name_codes: AllCodes = AllNameCodes().get_all_codes

        self.doc = Document(f"Nautilus_Namecodes_{self.all_name_codes.scheme_version}")

    @property
    def document(self) -> Document:
        """Return Document"""
        return self.doc

    def append_docuemnt(self, elements: Iterable[Element]) -> None:
        """Add to Class Document"""

        element: Element
        for element in elements:
            assert isinstance(element, Element)
            self.doc.add_element(element)

    def generate_blocks_list(self) -> Iterable[Element]:
        """Generate Basic List of Blocks, and their Sections and Codes."""

        blocks_list: List[Element] = []

        planes: Iterable[PlaneCodes] = self.all_name_codes.planes
        plane: PlaneCodes

        for plane in planes:
            blocks: Iterable[BlockCodes] = plane.blocks
            block: BlockCodes

            for block in blocks:
                blocks_list += self.build_block(block)

        return blocks_list

    def generate_sections_list(self) -> Iterable[Element]:
        """Generate Basic list of All Sections, with their Codes."""

        sections_list: List[Element] = []

        planes: Iterable[PlaneCodes] = self.all_name_codes.planes
        plane: PlaneCodes

        for plane in planes:
            blocks: Iterable[BlockCodes] = plane.blocks
            block: BlockCodes

            for block in blocks:
                sections: Iterable[SectionCodes] = block.sections
                section: SectionCodes

                for section in sections:
                    sections_list += self.build_section(section)

        return sections_list

    def build_tree(self) -> Iterable[Element]:
        """Generate a Tree Output for the Console"""

        output: str = ""

        output += f"\nScheme Version: {self.all_name_codes.scheme_version}\n"

        output += f"\n.{self.all_name_codes.name:29}"
        output += f" ((({self.all_name_codes.gen_output_range()})))\n"

        plane: PlaneCodes
        plane_last: PlaneCodes = self.all_name_codes.planes[-1]

        for plane in self.all_name_codes.planes:

            plane_joiner: str = ("├──", "└──")[plane == plane_last]
            block_spacer: str = ("│   ", "    ")[plane == plane_last]

            output += f"│   \n{plane_joiner} {plane.name:27}"
            output += f" (({plane.gen_output_range()}))\n"

            block: BlockCodes
            block_last: BlockCodes = plane.blocks[-1]

            for block in plane.blocks:

                block_joiner: str = (f"{block_spacer}├──", f"{block_spacer}└──")[
                    block == block_last
                ]
                section_spacer: str = (f"{block_spacer}│   ", f"{block_spacer}    ")[
                    block == block_last
                ]

                output += f"{block_joiner} {block.name:24}"
                output += f" ({block.gen_output_range()})\n"

                section: SectionCodes
                section_last: SectionCodes = block.sections[-1]

                for section in block.sections:

                    section_joiner: str = (
                        f"{section_spacer}├──",
                        f"{section_spacer}└──",
                    )[section == section_last]

                    output += f"{section_joiner} {section.name:21}"
                    output += f" {section.gen_output_range()}\n"

                    output += ("", f"{section_spacer}\n")[section == section_last]

        return [Paragraph([InlineText(output)], code=True)]

    @staticmethod
    def build_block(block: BlockCodes) -> Iterable[Element]:
        """Given a Block, List it's sections and Codes."""

        block_title: Header = Header(text=InlineText(block.name), level=2)
        block_description: Paragraph = Paragraph(
            content=[InlineText(str(block.description), italics=True)]
        )
        block_range: Paragraph = Paragraph(
            content=[InlineText(block.gen_output_range())]
        )

        codes_table_title: List[InlineText] = [
            InlineText("Code"),
            InlineText("Name"),
        ]

        codes_data: List[Iterable[InlineText]] = []

        sections: Iterable[SectionCodes] = block.sections
        section: SectionCodes
        section_last: SectionCodes = block.sections[-1]

        for section in sections:
            codes_data.append(
                [InlineText(""), InlineText(section.gen_output_range(), italics=True)]
            )

            section_items: Tuple[int, str]
            for section_items in section.codes.items():

                code = InlineText(f"0x{section_items[0]:=04X}")
                name = InlineText(section_items[1])

                code_data: List[InlineText] = [code, name]

                codes_data.append(code_data)

            if section != section_last:
                codes_data.append([InlineText(""), InlineText("")])

        block_table: Table = Table(header=codes_table_title, body=codes_data)

        return [block_title, block_description, block_range, block_table]

    @staticmethod
    def build_section(section: SectionCodes) -> Iterable[Element]:
        """Given a Sections, List it's codes."""

        title: Header = Header(text=InlineText(section.name), level=3)
        description: Paragraph = Paragraph(
            content=[InlineText(str(section.description))]
        )
        codes_table_title: List[InlineText] = [
            InlineText("Code"),
            InlineText("Name"),
        ]
        codes_data: List[Iterable[InlineText]] = []

        codes_data.append(
            [InlineText(""), InlineText(section.gen_output_range(), italics=True)]
        )

        section_items: Tuple[int, str]

        for section_items in section.codes.items():

            code = InlineText(f"0x{section_items[0]:=04X}")
            name = InlineText(section_items[1])

            code_data: List[InlineText] = [code, name]

            codes_data.append(code_data)

        codes: Table = Table(header=codes_table_title, body=codes_data)

        return [title, description, codes]

    def build_codes(self) -> Iterable[Element]:
        """List All the Codes."""

        title: Header = Header(text=InlineText(self.all_name_codes.name), level=1)
        description: Paragraph = Paragraph(
            content=[InlineText(str(self.all_name_codes.description))]
        )
        codes_table_title: List[InlineText] = [
            InlineText("Code"),
            InlineText("Name"),
        ]
        codes_data: List[Iterable[InlineText]] = []

        code_item: Tuple[int, str]

        for code_item in self.all_name_codes.codes.items():

            code = InlineText(f"0x{code_item[0]:=04X}")
            name = InlineText(code_item[1])

            code_data: List[InlineText] = [code, name]

            codes_data.append(code_data)

        codes: Table = Table(header=codes_table_title, body=codes_data)

        return [title, description, codes]


if __name__ == "__main__":
    markdown_output: MarkdownOutput = MarkdownOutput()
    markdown_output.append_docuemnt(elements=markdown_output.build_codes())

    print(markdown_output.document.render())
