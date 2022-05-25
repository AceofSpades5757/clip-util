""" Going to try and set HTML.

First need to finish setting up setting text.

SUCCESS
Both text, AND html now works!!!

Note
----
The \x00\x00 bytes are _actually_ a single null-terminated string for unicode strings
with windows, and is a single \u0000, in Python which is 2 \x00 values.
"""
import platform
import unittest

from clipboard import Clipboard  # type: ignore
from clipboard import ClipboardFormat
from clipboard import HTMLClipboard


# Platform Settings
if platform.system() == "Windows":
    ...
elif platform.system() == "Linux":
    raise unittest.SkipTest("Platform not supported, but is planned.")
    raise NotImplementedError(
        f"Unsupported platform {platform.system()}, but definetly preferred."
    )
else:
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")


class TestMore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        content: str = """<h1>Hello World</h1>"""
        html_clipboard = HTMLClipboard(content)
        template: str = html_clipboard.generate_template()
        cls.template: str = template

        content = """
        <h1>Hello World!</h1>
        <p>This is a paragraph...</p>"""
        html_clipboard = HTMLClipboard(content)
        template_2: str = html_clipboard.generate_template()
        cls.template_2: str = template_2

    def test_basic_text(self) -> None:

        # Basic Text
        with Clipboard() as clipboard:
            clipboard["text"] = "Hello!"
            clipboard_data = clipboard["text"]

        self.assertTrue(bool(clipboard_data))

    @unittest.skip("CF_HTML is not supported on Windows (it should be).")
    def test_cf_html_format(self) -> None:

        format = ClipboardFormat.CF_HTML
        template = self.template  # type: ignore

        # Format: CF_HTML
        with Clipboard(format=format) as clipboard:
            handle = clipboard.set_clipboard(template, format)
            self.assertTrue(bool(handle))
            self.assertIn(format, clipboard.available_formats())

        with Clipboard(format=format) as clipboard:
            clipboard["html"] = template

        # Get Data
        with Clipboard() as clipboard:
            clipboard_data: str = clipboard[format]
            self.assertTrue(bool(clipboard_data))

    def test_html_format(self) -> None:

        format = ClipboardFormat.HTML_Format
        template = self.template  # type: ignore

        # Format: HTML
        with Clipboard(format=format) as clipboard:
            handle = clipboard.set_clipboard(template, format)
            self.assertTrue(bool(handle))
            self.assertIn(format, clipboard.available_formats())

        with Clipboard(format=format) as clipboard:
            clipboard["html"] = template

        # Get Data
        with Clipboard() as clipboard:
            clipboard_data_1: str = clipboard[format]
            self.assertTrue(bool(clipboard_data_1))

        # Get Data 2
        with Clipboard() as clipboard:
            clipboard_data_2: str = clipboard["html"]
            self.assertTrue(bool(clipboard_data_2))

        # No Format originally
        with Clipboard() as clipboard:
            clipboard["html"] = template
            clipboard_data_3: str = clipboard["html"]
            self.assertTrue(bool(clipboard_data_3))


if __name__ == "__main__":
    unittest.main()
