import platform
import unittest

from clipboard import ClipboardFormat
from clipboard import HTML_ENCODING
from clipboard import HTMLClipboard


# Platform Settings
if platform.system() != "Windows":
    html_type_1 = ClipboardFormat.HTML_Format
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")


class TestHTMLClipboard(unittest.TestCase):
    def test_simple(self) -> None:
        html_content: str = """<h1>Hello World</h1>"""

        html_clipboard = HTMLClipboard(html_content)

        template: str = html_clipboard.generate_template()
        raw: bytes = html_clipboard.raw  # encoding of content

        self.assertTrue(bool(template))
        self.assertEqual(html_content.encode(HTML_ENCODING), raw)


if __name__ == "__main__":
    unittest.main()
