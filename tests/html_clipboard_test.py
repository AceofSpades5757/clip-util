import platform
import unittest

from clipboard import HTML_ENCODING
from clipboard import ClipboardFormat
from clipboard import HTMLTemplate
from clipboard import get_clipboard
from clipboard import set_clipboard


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

if __name__ == "__main__":
    unittest.main()
