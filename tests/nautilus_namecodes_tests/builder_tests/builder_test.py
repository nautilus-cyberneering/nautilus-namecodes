"""Testing Namecode Building Infrastructure"""

# pylint: disable=too-many-instance-attributes

import unittest

from nautilus_namecodes.builder.namecode_builder_dataclasses import (
    Block,
    Plane,
    Section,
)
from nautilus_namecodes.namecodes_dataclasses import (
    BlockCodes,
    PlaneCodes,
    SectionCodes,
)


class SectionStaticTestCase(unittest.TestCase):
    """Test Static Function in Section"""

    def setUp(self) -> None:
        self.value_list = Section.generate_pages_of_values(
            base_name="f",
            pages_to_use=1,
            gen_format="{name}:{value:02X}",
        )

    def test_generate_pages_of_values(self):
        """Test: 'Section.generate_pages_of_values'"""
        self.assertEqual(len(self.value_list), 0x00F)
        self.assertEqual(
            self.value_list,
            [
                "f:01",
                "f:02",
                "f:03",
                "f:04",
                "f:05",
                "f:06",
                "f:07",
                "f:08",
                "f:09",
                "f:0A",
                "f:0B",
                "f:0C",
                "f:0D",
                "f:0E",
                "f:0F",
            ],
        )


class SectionTestCase(unittest.TestCase):
    """Test Instance of the Section Class"""

    def setUp(self) -> None:
        self.section: Section = Section(
            name="Test Section",
            description="Test",
            values=["Test", "One", "Two"],
        )

        self.section_codes: SectionCodes = self.section.get_section_codes(0x100)

        return super().setUp()

    def test_section(self):
        """Test Section Instance"""
        self.assertEqual(self.section.name, "Test Section")
        self.assertEqual(self.section.values, ["Test", "One", "Two"])
        self.assertEqual(self.section.get_pages_allocated(), 1)

    def test_section_codes(self):
        """Test Created SectionCodes"""
        self.assertEqual(self.section_codes.name, "Test Section")
        self.assertEqual(self.section_codes.codepoints_allocated, range(0x100, 0x10F))
        self.assertEqual(
            self.section_codes.codes,
            {
                0x100: "(Test Section) Test",
                0x101: "(Test Section) One",
                0x102: "(Test Section) Two",
            },
        )


class BlockTestCase(unittest.TestCase):
    """Test Instance of the Block Class"""

    def setUp(self) -> None:

        self.section: Section = Section(
            name="S1", description="Test", values=["Block", "Test", "Section"]
        )
        self.section2: Section = Section(
            name="S2", description="Test", values=["Block", "Second", "Section"]
        )

        self.section3: Section = Section(
            name="S3", description="Test", values=["Block", "Third", "Section"]
        )

        self.section_list: list[Section] = list(
            [self.section, self.section2, self.section3]
        )

        self.block: Block = Block(
            name="TestBlock", description="Test", sections=self.section_list
        )
        self.blockcodes: BlockCodes = self.block.get_block_codes(0x100)

    def test_block(self):
        """Test Block Instance"""
        self.assertEqual(self.block.name, "TestBlock")
        self.assertEqual(self.block.get_page_allocations(), [1, 1, 1])
        self.assertEqual(self.block.get_pages_allocated(), 3)
        self.assertEqual(self.block.sections, self.section_list)

    def test_block_codes(self):
        """Test Created BlockCodes"""
        self.assertEqual(self.blockcodes.name, "TestBlock")
        self.assertEqual(self.blockcodes.codepoints_allocated, range(0x100, 0x12F))
        self.assertEqual(len(self.blockcodes.sections), len(self.section_list))
        self.assertEqual(len(self.blockcodes.codes), 9)
        self.assertEqual(
            self.blockcodes.codes,
            {
                0x100: "(S1) Block",
                0x101: "(S1) Test",
                0x102: "(S1) Section",
                0x110: "(S2) Block",
                0x111: "(S2) Second",
                0x112: "(S2) Section",
                0x120: "(S3) Block",
                0x121: "(S3) Third",
                0x122: "(S3) Section",
            },
        )


class PlaneTestCase(unittest.TestCase):
    """Test Instance of the Plane Class"""

    def setUp(self) -> None:

        self.section: Section = Section(
            name="S1", description="Test", values=["Plane", "Test", "Section"]
        )
        self.section2: Section = Section(
            name="S2", description="Test", values=["Plane", "Second", "Section"]
        )

        self.section_list: list[Section] = list([self.section, self.section2])

        self.section_list2: list[Section] = list([self.section, self.section2])

        self.block: Block = Block(
            name="TestPlane", description="Test", sections=self.section_list
        )
        self.block2: Block = Block(
            name="TestPlane2", description="Test", sections=self.section_list2
        )

        self.block_list: list[Block] = list([self.block, self.block2])

        self.plane: Plane = Plane(
            name="TestPlane", description="Test", blocks=self.block_list
        )

        self.planecodes: PlaneCodes = self.plane.get_plane_codes(0x100)

    def test_plane(self):
        """Test Plane Instance"""
        self.assertEqual(self.plane.name, "TestPlane")
        self.assertEqual(self.plane.get_block_page_allocations(), [2, 2])
        self.assertEqual(self.plane.get_pages_allocated(), 4)
        self.assertEqual(self.plane.blocks, self.block_list)

    def test_block_codes(self):
        """Test Created BlockCodes"""
        self.assertEqual(self.planecodes.name, "TestPlane")
        self.assertEqual(self.planecodes.codepoints_allocated, range(0x100, 0x13F))
        self.assertEqual(len(self.planecodes.blocks), len(self.section_list))
        self.assertEqual(len(self.planecodes.codes), 12)
        self.assertEqual(
            self.planecodes.codes,
            {
                0x100: "(S1) Plane",
                0x101: "(S1) Test",
                0x102: "(S1) Section",
                0x110: "(S2) Plane",
                0x111: "(S2) Second",
                0x112: "(S2) Section",
                0x120: "(S1) Plane",
                0x121: "(S1) Test",
                0x122: "(S1) Section",
                0x130: "(S2) Plane",
                0x131: "(S2) Second",
                0x132: "(S2) Section",
            },
        )


if __name__ == "__main__":
    unittest.main()
