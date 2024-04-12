This branch is designed to verify capacity of setting the clipboard data with images.

- [ ] FIXME: Need to refactor to allow for bytes to be copied to clipboard.
- [ ] Add tests for setting clipboard data with images.
- [ ] Add section in README for setting clipboard data with images.
- [ ] Copy README to readme test.
- [ ] Copy README to docs/source/quickstart.rst

```python
import io

from clipboard import *

import win32clipboard
from PIL import Image


# required `Pillow` package for testing
# TODO: Get bytes data so we don't need the dependency for testing.
#   Or just add it to the `test` extra.
with Image.open(png_file) as img:
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    # TODO: Why 14?
    data = output.getvalue()[14:]
    output.close()

    # Here is what we want to replace
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    # With this
    with Clipboard() as cb:
        cb.set_clipboard(data, ClipboardFormat.CF_DIB)
        # Mime types (idea)
        cb.set_clipboard(data, "image/png")
        cb.set_clipboard(data, "image/jpeg")
        cb.set_clipboard(data, "image/gif")
        # Alternative APIs (idea)
        cb.set_image(img)
        cb.set_image(data)
        cb.set_image(path)
    # OR this
    set_clipboard(data, ClipboardFormat.CF_DIB)
    # Mime types (idea)
    set_clipboard(data, "image/png")
    set_clipboard(data, "image/jpeg")
    set_clipboard(data, "image/gif")
    # Alternative APIs (idea)
    set_image(img)
```

Here is the inspiration. I'd like to replace the `win32clipboard` code with `clip-util`.

```python
#!/usr/bin/env pip-run
"""Takes a PNG file, adds a white background to it, and copies it to the
clipboard.

Uses `pip-run` to run the script with the required packages installed.
"""
__requires__ = ["Pillow", "pywin32"]

import io
import sys
from pathlib import Path
from typing import TypeAlias
from typing import Union

import win32clipboard
from PIL import Image


PathLike = Union[str, bytes, Path]
RGBA: TypeAlias = tuple[int, int, int, int]


def add_white_bg_to_png(
    png_file: PathLike,
    copy: bool = True,
    open: bool = False,
    background_color: RGBA = (255, 255, 255, 255),
) -> None:
    """Add a white background to a PNG file and copy it to the clipboard."""
    with Image.open(png_file) as img:
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, background_color)
        img = Image.alpha_composite(bg, img)

        # Copy to clipboard
        if copy:
            output = io.BytesIO()
            img.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

        # Open the image
        if open:
            img.show()
        print("Image copied to clipboard.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <png_file>")
        print(
            "Takes a PNG file and adds a white background to it, copying it to the clipboard."
        )
        raise SystemExit(1)

    add_white_bg_to_png(sys.argv[1])
```
