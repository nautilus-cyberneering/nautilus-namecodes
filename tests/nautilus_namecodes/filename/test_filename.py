"""Filename Testing"""

from typing import Dict

import pytest

from nautilus_namecodes.namecodes_dataclasses import AllCodes
from nautilus_namecodes.parser.filename_data import ParseFilename
from nautilus_namecodes.scheme.v_0_1_0.filename import (
    DataType,
    Extension,
    Filename,
    Gold,
    GoldAlternative,
    GoldAlternativeBase,
    GoldAlternativeBaseVariant,
    GoldBase,
    GoldBaseVariant,
    ItemNumber,
    LibraryEntry,
    LibraryName,
    Listing,
    Modification,
    Modifications,
    Ways,
    mk_modifications,
)
from nautilus_namecodes.scheme.v_0_1_0.filename_model import (
    NautilusNamecodesFilenameBaseModel,
)
from nautilus_namecodes.scheme.v_0_1_0.namecodes import AllNameCodes


@pytest.fixture(name="all_codes")
def fixture_all_codes() -> AllCodes:
    """Basic Fixture that returns the All Codes Dataclass"""

    return AllNameCodes().get_all_codes


@pytest.fixture(name="modifications")
def fixture_modifications() -> Dict[str, Modifications]:
    """Test Fixture of a Dictionary of Modifications"""

    return {
        "A": mk_modifications(
            [
                Modification("Adaption", "prospective", "bottom"),
            ]
        ),
        "AB": mk_modifications(
            [
                Modification("Adaption", "prospective", "bottom"),
                Modification("Adaption", "prospective", "top"),
            ]
        ),
        "BA": mk_modifications(
            [
                Modification("Adaption", "prospective", "top"),
                Modification("Adaption", "prospective", "bottom"),
            ]
        ),
    }


@pytest.fixture(name="golds")
def fixture_golds(modifications: Dict[str, Modifications]) -> Dict[str, Gold]:
    """Fixture to Return Constructed 'Gold' Classes"""

    return {
        "Gold": Gold(Ways.GOLD),
        "GoldAlternative": Gold(
            GoldAlternative(modifications["A"], Ways.GOLD_ALTERNATIVE)
        ),
        "GoldAlternativeBase": Gold(
            GoldAlternative(
                modifications["AB"],
                GoldAlternativeBase(Ways.GOLD_ALTERNATIVE_BASE),
            )
        ),
        "GoldAlternativeBaseVariant": Gold(
            GoldAlternative(
                modifications["BA"],
                GoldAlternativeBase(GoldAlternativeBaseVariant(modifications["A"])),
            )
        ),
        "GoldBase": Gold(GoldBase(Ways.GOLD_BASE)),
        "GoldBaseVariant": Gold(GoldBase(GoldBaseVariant(modifications["A"]))),
    }


@pytest.fixture(name="filenames")
def fixture_filenames(golds: Dict[str, Gold]) -> Dict[str, Filename]:
    """Fixture that returns a set of test Filenames."""

    library_entry = LibraryEntry(LibraryName("aaa"), ItemNumber(0x001))
    listing: Listing = Listing(0x001, 0x001)
    data_type: DataType = DataType("Index")
    extention = Extension("test.time")

    filenames: Dict[str, Filename] = {}

    for gold in golds.items():
        filenames |= {
            gold[0]: Filename(
                library_entry,
                listing,
                gold[1],
                data_type,
                extention,
            ),
        }

    return filenames


def test_filenames(all_codes: AllCodes, filenames: Dict[str, Filename]) -> None:
    """Test if the Filenames Fixtures is working"""

    for filename in filenames.items():
        filename_str: str = filename[1].get_filename(all_codes)
        new_filename: Filename = ParseFilename.parse_filename(all_codes, filename_str)
        new_filename_str: str = new_filename.get_filename(all_codes)

        print(new_filename_str)

        if filename_str != new_filename_str:
            raise AssertionError(
                f"The original {filename_str} is not the same as the regenerated {new_filename_str}!"
            )

        if filename[1] != new_filename:
            raise AssertionError(
                f"The original {filename[1]} is not the same as the regenerated {new_filename}!"
            )


def test_filenames_json(filenames: Dict[str, Filename]) -> None:
    """Test if the Filenames Fixtures is working"""

    for filename in filenames.items():
        print(NautilusNamecodesFilenameBaseModel(encoding=filename[1]).json())


def test_filename_schema() -> None:
    """Test Generation of the Json Schema"""
    print(NautilusNamecodesFilenameBaseModel.schema_json())
