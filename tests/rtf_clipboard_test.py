"""RTF tests.

FIXME: There appear to be some race conditions with the clipboard.
    Tests will randomly fail at certain points.
    Should investigate and possibly add a delay to the tests, or a timeout in
    the API.
"""
import platform
import unittest

from clipboard import Clipboard
from clipboard import ClipboardFormat
from clipboard import get_clipboard
from clipboard import set_clipboard
from clipboard import get_available_formats


# Platform Settings
if platform.system() != "Windows":
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")


class TestRTFClipboard(unittest.TestCase):
    def test_simple(self) -> None:
        rtf: str = r"{\rtf1\ansi \b hello world \b0 }"

        handle = set_clipboard(rtf, ClipboardFormat.CF_RTF)
        self.assertTrue(bool(handle))
        paste = get_clipboard(ClipboardFormat.CF_RTF)
        self.assertEqual(rtf, paste)
        available = get_available_formats()
        self.assertIn(ClipboardFormat.CF_RTF, available)
        
        try:
            handle = set_clipboard(rtf, "rtf")
        except:
            breakpoint()
        self.assertTrue(bool(handle))
        paste = get_clipboard("rtf")
        self.assertEqual(rtf, paste)
        # 'rtf' is not in ClibpoardFormat
        available = get_available_formats()
        # self.assertIn(ClipboardFormat("rtf"), available)

    def test_rtf_context_manager(self) -> None:
        format = ClipboardFormat.CF_RTF
        content: str = (
            r"{\pard \ql \f0 \sa180 \li0 \fi0 Hello {\b World}!\par}"
        )

        # Standard
        with Clipboard(format=format) as clipboard:
            handle = clipboard.set_clipboard(content)
            self.assertTrue(bool(handle))
            available = clipboard.available_formats()
            self.assertIn(format, available)
            paste = clipboard.get_clipboard()
            self.assertEqual(content, paste)

        # Using Keys (ClipboardFormat)
        with Clipboard() as clipboard:
            clipboard[format] = content
            paste = clipboard[format]
            self.assertEqual(content, paste)
            available = clipboard.available_formats()
            self.assertIn(format, available)

        # Using Keys (string)
        with Clipboard() as clipboard:
            clipboard["rtf"] = content
            paste = clipboard["rtf"]
            self.assertEqual(content, paste)
            available = clipboard.available_formats()
            self.assertIn(format, available)

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