"""Format the Generated Namecodes for Console Presentation"""

from nautilus_namecodes.format.generate_markdown import MarkdownOutput
from nautilus_namecodes.scheme.v_0_1_0.namecode_model import (
    AllNameCodes,
    NautilusNamecodesListModel,
    NautilusNamecodesModel,
    NautilusNamecodesTreeModel,
    TreeStubGen,
)


class ConsoleOutput:
    """Generate Text Output suitable for the Console."""

    @staticmethod
    def generate_tree_output() -> str:
        """Generate a Full Output for the Console"""

        markdown_output: MarkdownOutput = MarkdownOutput()
        markdown_output.append_docuemnt(elements=markdown_output.build_tree())

        return markdown_output.document.render()

    @staticmethod
    def generate_blocks_output() -> str:
        """Generate a Full Output for the Console"""

        markdown_output: MarkdownOutput = MarkdownOutput()
        markdown_output.append_docuemnt(elements=markdown_output.generate_blocks_list())

        return markdown_output.document.render()

    @staticmethod
    def generate_codes_output() -> str:
        """Generate a Full Output for the Console"""

        markdown_output: MarkdownOutput = MarkdownOutput()
        markdown_output.append_docuemnt(elements=markdown_output.build_codes())

        return markdown_output.document.render()

    @staticmethod
    def generate_json_schema() -> str:
        """Generate Dataclass Json Schema"""

        nautilus_namecodes_model = NautilusNamecodesModel(
            data=AllNameCodes().get_all_codes
        )

        return nautilus_namecodes_model.schema_json()

    @staticmethod
    def generate_json() -> str:
        """Generate Dataclass as Json"""

        nautilus_namecodes_model = NautilusNamecodesModel(
            data=AllNameCodes().get_all_codes
        )

        return nautilus_namecodes_model.json()

    @staticmethod
    def generate_json_schema_tree() -> str:
        """Generate Stub Tree Json Schema"""

        nautilus_namecodes_tree_model = NautilusNamecodesTreeModel(
            data=TreeStubGen().tree_stub
        )

        return nautilus_namecodes_tree_model.schema_json()

    @staticmethod
    def generate_json_tree() -> str:
        """Generate Stub Tree as Json"""

        nautilus_namecodes_tree_model = NautilusNamecodesTreeModel(
            data=TreeStubGen().tree_stub
        )

        return nautilus_namecodes_tree_model.json()

    @staticmethod
    def generate_json_schema_codelist() -> str:
        """Generate Full Code List Json Schema"""

        nautilus_namecodes_model = NautilusNamecodesListModel(
            namecodes=AllNameCodes().get_all_codes.codes
        )

        return nautilus_namecodes_model.schema_json()

    @staticmethod
    def generate_json_codelist() -> str:
        """Generate Full Code List as Json"""

        nautilus_namecodes_model = NautilusNamecodesListModel(
            namecodes=AllNameCodes().get_all_codes.codes
        )

        return nautilus_namecodes_model.json()


if __name__ == "__main__2":
    print(ConsoleOutput.generate_tree_output())
    print(ConsoleOutput.generate_blocks_output())
    print(ConsoleOutput.generate_codes_output())
    print(ConsoleOutput.generate_json_schema_tree())
    print(ConsoleOutput.generate_json_schema())
    print(ConsoleOutput.generate_json_schema_codelist())
    print(ConsoleOutput.generate_json_tree())
    print(ConsoleOutput.generate_json())
    print(ConsoleOutput.generate_json_codelist())


if __name__ == "__main__":
    print(ConsoleOutput.generate_json_schema_tree())
    # print(ConsoleOutput.generate_json())
    # print(ConsoleOutput.generate_blocks_output())
