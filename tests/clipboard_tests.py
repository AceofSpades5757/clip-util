import platform
import unittest

from clipboard import Clipboard
from clipboard import ClipboardFormat


# Platform Settings
if platform.system() == 'Windows':
    html_type_1 = ClipboardFormat.HTML_Format
elif platform.system() == 'Linux':
    raise unittest.SkipTest('Platform not supported, but is planned.')
    raise NotImplementedError(
        f'Unsupported platform {platform.system()}, but definetly preferred.'
    )
else:
    raise unittest.SkipTest(f'Platform not supported {platform.system()}.')
    raise NotImplementedError(f'Unsupported platform {platform.system()}.')


class TestClipboard(unittest.TestCase):
    def test_available_formats(self) -> None:
        with Clipboard(format=ClipboardFormat.CF_UNICODETEXT) as clipboard:
            formats: list[int] = clipboard.available_formats()
            primary_format: int = formats[0]

            self.assertTrue(bool(formats))
            self.assertTrue(bool(primary_format))

    def test_set_clipboard(self) -> None:

        # No errors should be raised during these operations

        with Clipboard(format=ClipboardFormat.CF_UNICODETEXT) as clipboard:
            clipboard[ClipboardFormat.CF_UNICODETEXT] = 'Hello!'

        with Clipboard(format=ClipboardFormat.CF_UNICODETEXT) as clipboard:
            handle = clipboard.set_clipboard('Hey!')
            self.assertTrue(bool(handle))

        # Mutliple sets
        with Clipboard(format=ClipboardFormat.CF_UNICODETEXT) as clipboard:
            for _ in range(3):
                handle = clipboard.set_clipboard('Hi!')
                self.assertTrue(bool(handle))

    def test_empty(self) -> None:
        with Clipboard() as clipboard:
            clipboard.empty()


if __name__ == '__main__':
    unittest.main()
