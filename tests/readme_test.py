import platform
import random
import string
import unittest
from typing import List

from clipboard import Clipboard
from clipboard import ClipboardFormat
from clipboard import get_clipboard
from clipboard import set_clipboard


# Platform Settings
if platform.system() == "Windows":
    html_type_1 = ClipboardFormat.HTML_Format
elif platform.system() == "Linux":
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")
else:
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")


class TestReadme(unittest.TestCase):
    def test_usage_clipboard(self) -> None:
        """https://github.com/AceofSpades5757/clip-util?tab=readme-ov-file#clipboard"""
        from clipboard import Clipboard


        clipboard = Clipboard()

        # Set Clipboard
        clipboard['text'] = 'Hello World!'
        # OR
        clipboard.set_clipboard('Hello World!')

        # Get Clipboard
        text = clipboard['text']
        # OR
        text = clipboard.get_clipboard('text')

        # Supports HTML
        clipboard['html'] = '<h1>Hello World</h1>'

    def test_usage_clipboard_context_manaager(self) -> None:
        """https://github.com/AceofSpades5757/clip-util?tab=readme-ov-file#context-manager"""
        from clipboard import Clipboard


        with Clipboard() as clipboard:

            # Set Clipboard
            clipboard['text'] = 'Hello World!'
            # OR
            clipboard.set_clipboard('Hello World!')

            # Get Clipboard
            text = clipboard['text']
            # OR
            text = clipboard.get_clipboard('text')

            # HTML
            clipboard['html'] = '<h1>Hello World</h1>'

    def test_clipboard_formats(self) -> None:
        """https://github.com/AceofSpades5757/clip-util?tab=readme-ov-file#clipboard-formats"""
        from clipboard import Clipboard
        from clipboard import ClipboardFormat
        from clipboard import HTMLTemplate


        with Clipboard() as clipboard:

            # Get All Available Formats
            format_ids: list[int] = clipboard.available_formats()

            # Get Specific Format by ID
            # Use parentheses to access the format
            formats: list[ClipboardFormat] = []
            for format_id in format_ids:
                if format_id in ClipboardFormat:
                    format: ClipboardFormat = ClipboardFormat(format_id)
                    formats.append(format)
                else:
                    # Format is not supported directly by this library
                    pass

            # Get Specified Format by Name
            # Use bracket notation to access the format
            format_name: str
            for format_name in [f.name for f in formats]:
                if format_name in ClipboardFormat:
                    format: ClipboardFormat = ClipboardFormat[format_name]
                    name: str = format.name
                else:
                    # Format is not supported directly by this library
                    pass

if __name__ == "__main__":
    unittest.main()
