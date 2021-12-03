"""Format the Generated Namecodes for Console Presentation"""

from nautilus_namecodes.format.generate_markdown import MarkdownOutput


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


if __name__ == "__main__":
    print(ConsoleOutput.generate_tree_output())
    print(ConsoleOutput.generate_blocks_output())
    print(ConsoleOutput.generate_codes_output())
