import platform
import unittest

from clipboard import Clipboard
from clipboard import ClipboardFormat
from clipboard import get_clipboard
from clipboard import set_clipboard
from clipboard.html_clipboard import HTMLTemplate

# Platform Settings
if platform.system() != "Windows":
    html_type_1 = ClipboardFormat.HTML_Format
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")


class TestHTMLClipboard(unittest.TestCase):
    def test_simple(self) -> None:
        html: str = "<h1>Hello World</h1>"

        template: HTMLTemplate = HTMLTemplate(html)

        final: str = template.generate()

        self.assertIn(html, final)
        self.assertTrue(bool(template))

    def test_set_and_get(self) -> None:
        html: str = "<h1>Hello World</h1>"
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML

        set_clipboard(html, format_)
        self.assertEqual(get_clipboard(format_), template.generate())

    def test_body(self) -> None:
        html: str = "<body><h1>Hello World</h1></body>"
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML

        set_clipboard(html, format_)
        self.assertEqual(get_clipboard(format_), template.generate())

    def test_html_and_body(self) -> None:
        html: str = "<html><body><h1>Hello World</h1></body></html>"
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML

        set_clipboard(html, format_)
        self.assertEqual(get_clipboard(format_), template.generate())

    def test_html_and_head_and_body(self) -> None:
        html: str = (
            "<html><head></head><body><h1>Hello World</h1></body></html>"
        )
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML

        set_clipboard(html, format_)
        self.assertEqual(get_clipboard(format_), template.generate())

    def test_html_generation(self) -> None:
        """Check to see that the HTML generation works as expected."""
        html: str = (
            "<html><head></head><body><h1>Hello World</h1></body></html>"
        )
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML
        generated: str = template.generate()

        assert bool(generated)
        # FIXME: Windows has different line endings (2 bytes) vs Linux (1 byte)
        # start html: 100 with Linux, 105 with Windows
        # end html: 229 with Linux, 240 with Windows
        # start fragment (after comment): 135 with Linux, 142 with Windows
        # end fragment (before comment): 194 with Linux, 203 with Windows
        assert generated == """\
Version:1.0
StartHTML:0000000100
EndHTML:0000000229
StartFragment:0000000135
EndFragment:0000000194
<html>
<body>
<!--StartFragment-->
<html><head></head><body><h1>Hello World</h1></body></html>
<!--EndFragment-->
</body>
</html>"""


class TestMore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        content: str = """<h1>Hello World</h1>"""
        html_clipboard = HTMLTemplate(content)
        template: str = html_clipboard.generate()
        cls.template: str = template

        content = """
        <h1>Hello World!</h1>
        <p>This is a paragraph...</p>"""
        html_clipboard = HTMLTemplate(content)
        template_2: str = html_clipboard.generate()
        cls.template_2: str = template_2

    def test_basic_text(self) -> None:
        # Basic Text
        with Clipboard() as clipboard:
            clipboard["text"] = "Hello!"
            clipboard_data = clipboard["text"]

        self.assertTrue(bool(clipboard_data))

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

    @unittest.skip(
        "There have been a bunch of issues with this format suddenly."
    )
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
