"""temp test for issue #28
from clipboard import Clipboard

with Clipboard() as clipboard:
    clipboard.set_clipboard("<html><body><b>hello world</b><body></html>", 'html')
    print(clipboard.available_formats())

with Clipboard() as clipboard:
    print(clipboard['html'])
"""
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
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")
else:
    raise unittest.SkipTest(f"Platform not supported {platform.system()}.")
    raise NotImplementedError(f"Unsupported platform {platform.system()}.")


class TestIssue28(unittest.TestCase):
    def test_issue_28(self) -> None:
        from clipboard import Clipboard

        """
        with Clipboard() as clipboard:
            clipboard.set_clipboard("<html><body><b>hello world</b><body></html>", 'html')
            # We get [0, 49418] on Windows
            # 0 = ?
            # 49418 = HTML_Format
            print(clipboard.available_formats())
            self.assertTrue(bool(clipboard.available_formats()))
            self.assertEqual(clipboard.available_formats(), [49418, 0])
            for format_id in clipboard.available_formats():
                try:
                    format: ClipboardFormat = ClipboardFormat(format_id)
                except ValueError:
                    print(f"Format {format_id} not found.")
                    continue
                name: str = format.name
                print(f"{name} = {format}")

        with Clipboard() as clipboard:
            print(clipboard['html'])
        """


        # actual testing
        # content: str = "<html><body><b>hello world</b><body></html>"
        # content: str = "<body><b>hello world</b><body>"
        content: str = "<b>hello world</b>"
        post = None
        with Clipboard() as clipboard:
            # Set
            clipboard.set_clipboard(content, 'html')
            post = clipboard['html']
            print(post)
        breakpoint()
        self.assertEqual(content, post)


if __name__ == "__main__":
    unittest.main()
