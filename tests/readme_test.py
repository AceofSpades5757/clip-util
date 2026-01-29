import platform
import unittest

from clipboard import Clipboard
from clipboard import ClipboardFormat
from clipboard import get_clipboard
from clipboard import set_clipboard


# Platform Settings
if platform.system() == "Windows":
    html_type_1 = ClipboardFormat.HTML_Format
elif platform.system() == "Linux":
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
else:
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")


class TestReadme(unittest.TestCase):
    def test_usage_clipboard(self) -> None:
        """https://github.com/AceofSpades5757/clip-util?tab=readme-ov-file#clipboard"""

        clipboard = Clipboard()

        # Set Clipboard
        clipboard["text"] = "Hello World!"
        # OR
        clipboard.set_clipboard("Hello World!")

        # Get Clipboard
        text = clipboard["text"]
        # OR
        text = clipboard.get_clipboard("text")

        # Supports HTML
        clipboard["html"] = "<h1>Hello World</h1>"

    def test_usage_clipboard_context_manaager(self) -> None:
        """https://github.com/AceofSpades5757/clip-util?tab=readme-ov-file#context-manager"""

        with Clipboard() as clipboard:
            # Set Clipboard
            clipboard["text"] = "Hello World!"
            # OR
            clipboard.set_clipboard("Hello World!")

            # Get Clipboard
            text = clipboard["text"]
            # OR
            text = clipboard.get_clipboard("text")

            # HTML
            clipboard["html"] = "<h1>Hello World</h1>"

    def test_clipboard_formats(self) -> None:
        """https://github.com/AceofSpades5757/clip-util?tab=readme-ov-file#clipboard-formats"""
        from clipboard import ClipboardFormat
        from clipboard import get_format_name

        with Clipboard() as clipboard:
            # Get All Available Formats
            format_ids: list[int] = clipboard.available_formats()

            # Get Specific Format by ID
            # Use parentheses to access the format by ID
            formats: list[ClipboardFormat] = []
            format_id: int
            for format_id in format_ids:
                if format_id in ClipboardFormat:
                    format: ClipboardFormat = ClipboardFormat(format_id)
                    formats.append(format)
                else:
                    # Format is not supported directly by this library
                    pass

            # Get Specified Format by Name (directly)
            format_names: list[str] = []
            format_id: int
            for format_id in format_ids:
                name: str = get_format_name(format_id)
                format_names.append(name)

            # Get Specified Format by Name (using enum)
            # Use bracket notation to access the format
            #
            # Note: this method is not as robust as using `get_format_name`
            formats: list[ClipboardFormat] = []
            format_names: list[str] = []
            format_name: str
            for format_name in [f.name for f in formats]:
                if format_name in ClipboardFormat:
                    format: ClipboardFormat = ClipboardFormat[format_name]
                    name: str = format.name
                    formats.append(format)
                    format_names.append(name)
                else:
                    # Format is not supported directly by this library
                    pass

    def test_get_all_supported_formats(self) -> None:
        """https://github.com/AceofSpades5757/clip-util?tab=readme-ov-file#get-all-supported-formats"""
        from clipboard import get_available_formats
        from clipboard import get_format_name

        set_clipboard("Hello World!")
        available: list[int] = get_available_formats()
        print(f"{available=}")

        for format_id in available:
            name: str = get_format_name(format_id)
            content: str = get_clipboard(format_id)
            print(f"{format_id=}", f"{name=}, {content=}")


if __name__ == "__main__":
    unittest.main()
