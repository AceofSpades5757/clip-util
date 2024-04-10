import platform
import unittest

from clipboard import HTML_ENCODING
from clipboard import ClipboardFormat
from clipboard import HTMLTemplate
from clipboard import get_clipboard
from clipboard import set_clipboard
from clipboard import Clipboard


# Platform Settings
if platform.system() != "Windows":
    html_type_1 = ClipboardFormat.HTML_Format
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")


class TestHTMLClipboard(unittest.TestCase):
    def test_simple(self) -> None:
        html: str = "<h1>Hello World</h1>"

        template: HTMLTemplate = HTMLTemplate(html)

        final: str = template.final()
        raw: bytes = template.bytes  # encoding of content

        self.assertTrue(bool(template))
        self.assertEqual(html.encode(HTML_ENCODING), raw)

    def test_set_and_get(self) -> None:
        html: str = "<h1>Hello World</h1>"
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML

        set_clipboard(html, format_)
        self.assertEqual(get_clipboard(format_), template.final())

    def test_body(self) -> None:
        html: str = "<body><h1>Hello World</h1></body>"
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML

        set_clipboard(html, format_)
        self.assertEqual(get_clipboard(format_), template.final())

    def test_html_and_body(self) -> None:
        html: str = "<html><body><h1>Hello World</h1></body></html>"
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML

        set_clipboard(html, format_)
        self.assertEqual(get_clipboard(format_), template.final())

    def test_html_and_head_and_body(self) -> None:
        html: str = "<html><head></head><body><h1>Hello World</h1></body></html>"
        template: HTMLTemplate = HTMLTemplate(html)
        format_: ClipboardFormat = ClipboardFormat.CF_HTML

        set_clipboard(html, format_)
        self.assertEqual(get_clipboard(format_), template.final())


class TestMore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        content: str = """<h1>Hello World</h1>"""
        html_clipboard = HTMLTemplate(content)
        template: str = html_clipboard.final()
        cls.template: str = template

        content = """
        <h1>Hello World!</h1>
        <p>This is a paragraph...</p>"""
        html_clipboard = HTMLTemplate(content)
        template_2: str = html_clipboard.final()
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

    def test_rtf_format(self) -> None:
        format = ClipboardFormat.CF_RTF
        content: str = (
            r"{\pard \ql \f0 \sa180 \li0 \fi0 Hello {\b World}!\par}"
        )

        # Format: RTF
        with Clipboard(format=format) as clipboard:
            handle = clipboard.set_clipboard(content, format)
            self.assertTrue(bool(handle))
            self.assertIn(format, clipboard.available_formats())

        with Clipboard(format=format) as clipboard:
            clipboard["rtf"] = content

        # Get Data
        with Clipboard() as clipboard:
            clipboard_data_1: str = clipboard[format]
            self.assertTrue(bool(clipboard_data_1))

        # Get Data 2
        with Clipboard() as clipboard:
            clipboard_data_2: str = clipboard["rtf"]
            self.assertTrue(bool(clipboard_data_2))

        # No Format originally
        with Clipboard() as clipboard:
            clipboard["rtf"] = content
            clipboard_data_3: str = clipboard["rtf"]
            self.assertTrue(bool(clipboard_data_3))


if __name__ == "__main__":
    unittest.main()
