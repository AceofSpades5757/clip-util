""" Test available formats for the clipboard """

import platform
import unittest

from clipboard import ClipboardFormat  # type: ignore


# Platform Settings
if platform.system() == "Windows":
    html_type_1 = ClipboardFormat.HTML_Format
elif platform.system() == "Linux":
    raise unittest.SkipTest("Platform not supported, but is planned.")
    raise NotImplementedError(
        f"Unsupported platform {platform.system()}, but definetly preferred."
    )
else:
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")


class TestInterface(unittest.TestCase):
    def test_simple(self) -> None:
        self.assertTrue(bool(ClipboardFormat.HTML_Format))
        self.assertTrue(bool(ClipboardFormat.CF_HTML))
        self.assertTrue(bool(ClipboardFormat["HTML_Format"]))


class TestFormats(unittest.TestCase):
    def test_simple(self) -> None:
        self.assertNotEqual("CF_HTML", ClipboardFormat.CF_HTML)
        self.assertNotEqual("HTML_Format", ClipboardFormat.HTML_Format)
        self.assertNotEqual("CF_HTML", ClipboardFormat.HTML_Format)

        self.assertEqual(html_type_1, ClipboardFormat.HTML_Format)

        self.assertTrue(bool(ClipboardFormat.CF_HTML))
        self.assertTrue(bool(ClipboardFormat.names))
        self.assertTrue(bool(ClipboardFormat.values))
        self.assertIn(1, ClipboardFormat.values)  # type: ignore
        self.assertIn(html_type_1, ClipboardFormat.values)  # type: ignore
        self.assertTrue(bool(ClipboardFormat.html))
        self.assertTrue(bool(ClipboardFormat.HTML))
        self.assertIn("CF_HTML", ClipboardFormat)
        self.assertIn("HTML_Format", ClipboardFormat)
        self.assertIn(ClipboardFormat.CF_HTML, ClipboardFormat)
