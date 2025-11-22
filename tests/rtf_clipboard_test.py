"""RTF tests."""

import platform
import unittest

from clipboard import Clipboard
from clipboard import ClipboardFormat
from clipboard import get_available_formats
from clipboard import get_clipboard
from clipboard import set_clipboard


# Platform Settings
if platform.system() != "Windows":
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")


class TestRTFClipboard(unittest.TestCase):
    def test_simple(self) -> None:
        rtf: str = r"{\rtf1\ansi \b hello world \b0 }"

        handle = set_clipboard(rtf, ClipboardFormat.CF_RTF)
        self.assertTrue(bool(handle))
        paste = get_clipboard(ClipboardFormat.CF_RTF)
        self.assertEqual(rtf, paste)
        available = get_available_formats()
        self.assertIn(ClipboardFormat.CF_RTF, available)

        handle = set_clipboard(rtf, "rtf")
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


if __name__ == "__main__":
    unittest.main()
