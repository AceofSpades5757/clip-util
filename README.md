[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![PyPI](https://img.shields.io/pypi/v/clip-util?color=darkred)](https://pypi.org/project/clip-util/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clip-util?label=Python%20Version&logo=python&logoColor=yellow)](https://pypi.org/project/clip-util/)
[![PyPI - License](https://img.shields.io/pypi/l/clip-util?color=green)](https://github.com/AceofSpades5757/clip-util/blob/main/LICENSE)

[![Tests](https://github.com/AceofSpades5757/clip-util/actions/workflows/test.yml/badge.svg)](https://github.com/AceofSpades5757/clip-util/actions/workflows/test.yml)

[![Read the Docs](https://img.shields.io/readthedocs/clip-util)](https://clip-util.readthedocs.io/en/latest/)

# Description

Package for accessing the clipboard with Python.

# Installation

`pip install clip-util`

# Features

_Windows Only_

Allows you to set text, RTF, and HTML to the clipboard on Windows. Any other format can also be specified using the format type integer, specified by Windows.

## Supported Clipboard Formats

- Text
- HTML
- RTF

# Usage

## Clipboard

Will open and close every time the values are set, or retrieved. It's better to use a context manager.

```python
from clipboard import Clipboard


clipboard = Clipboard()

# Set Clipboard
clipboard["text"] = "Hello World!"
# OR
clipboard.set_clipboard("Hello World!")

# Get Clipboard
text = clipboard["text"]
# OR
text = clipboard.get_clipboard("text")

# Supports HTML
clipboard["html"] = "<h1>Hello World</h1>"
```


### Context Manager

```python
from clipboard import Clipboard


with Clipboard() as clipboard:

    # Set Clipboard
    clipboard["text"] = "Hello World!"
    # OR
    clipboard.set_clipboard("Hello World!")

    # Get Clipboard
    text = clipboard["text"]
    # OR
    text = clipboard.get_clipboard("text")

    # HTML
    clipboard["html"] = "<h1>Hello World</h1>"
```

## Clipboard Formats

You can use `clip-util` to access the clipboard formats directly.

`ClipboardFormat`: Enum for clipboard formats.

`ClipboardFormat.CF_HTML`: Represents HTML format.

`ClipboardFormat.CF_RTF`: Represents RTF format.

```python
from clipboard import Clipboard
from clipboard import ClipboardFormat
from clipboard import get_format_name


with Clipboard() as clipboard:

    # Get All Available Formats
    format_ids: list[int] = clipboard.available_formats()

    # Get Specific Format by ID
    # Use parentheses to access the format by ID
    formats: list[ClipboardFormat] = []
    format_id: int
    for format_id in format_ids:
        if format_id in ClipboardFormat:
            format: ClipboardFormat = ClipboardFormat(format_id)
            formats.append(format)
        else:
            # Format is not supported directly by this library
            pass

    # Get Specified Format by Name (directly)
    format_names: list[str] = []
    format_id: int
    for format_id in format_ids:
        name: str = get_format_name(format_id)
        format_names.append(name)

    # Get Specified Format by Name (using enum)
    # Use bracket notation to access the format
    #
    # Note: this method is not as robust as using `get_format_name`
    formats: list[ClipboardFormat] = []
    format_names: list[str] = []
    format_name: str
    for format_name in [f.name for f in formats]:
        if format_name in ClipboardFormat:
            format: ClipboardFormat = ClipboardFormat[format_name]
            name: str = format.name
            formats.append(format)
            format_names.append(name)
        else:
            # Format is not supported directly by this library
            pass
```

## Get All Supported Formats

You can even get the content of all available formats currently in the clipboard.

```python
from clipboard import get_available_formats
from clipboard import get_format_name
from clipboard import get_clipboard


available: list[int] = get_available_formats()
print(f"{available=}")

for format_id in available:
    name: str = get_format_name(format_id)
    content: str = get_clipboard(format_id)
    print(f"{format_id=}", f"{name=}, {content=}")
```
