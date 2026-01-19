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
    raise unittest.SkipTest("Platform not supported, but is planned.")
else:
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")


class TestClipboard(unittest.TestCase):
    def test_available_formats(self) -> None:
        with Clipboard(format=ClipboardFormat.CF_UNICODETEXT) as clipboard:
            formats: List[int] = clipboard.available_formats()
            primary_format: int = formats[0]

            self.assertTrue(bool(formats))
            self.assertTrue(bool(primary_format))

    def test_set_clipboard(self) -> None:
        # No errors should be raised during these operations
        # Assuming that the get clipboard function is working
        # Assuming that the get clipboard function is working

        with Clipboard(format=ClipboardFormat.CF_UNICODETEXT) as clipboard:
            random_text = "".join(
                random.choice(string.ascii_letters + string.digits)
                for _ in range(random.randint(1, 100))
            )
            clipboard[ClipboardFormat.CF_UNICODETEXT] = random_text
            text = clipboard[ClipboardFormat.CF_UNICODETEXT]
            self.assertEqual(text, random_text)

        with Clipboard(format=ClipboardFormat.CF_UNICODETEXT) as clipboard:
            random_text = "".join(
                random.choice(string.ascii_letters + string.digits)
                for _ in range(random.randint(1, 100))
            )
            handle = clipboard.set_clipboard(random_text)
            self.assertTrue(bool(handle))
            text = clipboard[ClipboardFormat.CF_UNICODETEXT]
            self.assertEqual(text, random_text)

        # Mutliple sets
        with Clipboard(format=ClipboardFormat.CF_UNICODETEXT) as clipboard:
            for _ in range(3):
                random_text = "".join(
                    random.choice(string.ascii_letters + string.digits)
                    for _ in range(random.randint(1, 100))
                )
                handle = clipboard.set_clipboard(random_text)
                self.assertTrue(bool(handle))

                text = clipboard[ClipboardFormat.CF_UNICODETEXT]
                self.assertEqual(text, random_text)

    def test_convience_functions(self) -> None:
        # No errors should be raised during these operations
        # Assuming that the get clipboard function is working
        # Assuming that the get clipboard function is working

        format = ClipboardFormat.CF_UNICODETEXT
        random_text = "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(random.randint(1, 100))
        )
        set_clipboard(random_text, format)
        text = get_clipboard(format)
        self.assertEqual(text, random_text)

    def test_empty(self) -> None:
        # No errors should be raised during these operations

        with Clipboard() as clipboard:
            clipboard._empty()


if __name__ == "__main__":
    unittest.main()
