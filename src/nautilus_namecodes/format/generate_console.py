"""Format the Generated Namecodes for Console Presentation"""

from nautilus_namecodes.namecodes_dataclasses import (
    AllCodes,
    BlockCodes,
    PlaneCodes,
    SectionCodes,
)
from nautilus_namecodes.scheme.v_0_0_1.namecodes import AllNameCodes


class ConsoleOutput:
    """Generate Text Output suitable for the Console."""

    def __init__(self) -> None:
        self.all_name_codes: AllCodes = AllNameCodes().get_all_codes

    def gen_tree_output(self) -> str:
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

        return output

    def gen_full_output(self) -> str:
        """Generate a Full Output for the Console"""

        output: str = ""

        output += f"\nScheme Version: {self.all_name_codes.scheme_version}\n"

        out_format_section: str = "\n| {code:6} | {name:34}|"

        output += f"\nTitle: {self.all_name_codes.name}"
        output += f"\nCodes: {self.all_name_codes.gen_output_range()}\n"

        plane: PlaneCodes
        for plane in self.all_name_codes.planes:
            output += f"\nPlane: {plane.name}"
            output += f"\nCodes: {plane.gen_output_range()}\n"

            block: BlockCodes
            for block in plane.blocks:
                output += f"\nBlock: {block.name}"
                output += f"\nCodes: {block.gen_output_range()}\n"

                section: SectionCodes
                for section in block.sections:
                    output += out_format_section.format(
                        code="", name=section.gen_output_range()
                    )
                    item: tuple[int, str]
                    for item in section.codes.items():
                        output += out_format_section.format(
                            code=f"0x{item[0]:=04X}", name=item[1]
                        )

                    output += "\n"

        return output


if __name__ == "__main__":
    print(ConsoleOutput().gen_tree_output())
    print(ConsoleOutput().gen_full_output())
