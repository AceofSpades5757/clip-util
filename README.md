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

Allows for text and HTML on Windows.

## Supported Clipboard Formats

- Text
- HTML

# Usage

## Clipboard

Will open and close every time the values are set, or retrieved. It's better to use a context manager.

```python
from clipboard import Clipboard


clipboard = Clipboard()

# Set Clipboard
clipboard['text'] = 'Hello World!'
# OR
clipboard.set_clipboard('text') = 'Hello World!'

# Get Clipboard
text = clipboard['text']
# OR
text = clipboard.get_clipboard('text')
```

<!--

# HTML
clipboard['html'] = '<h1>Hello World</h1>'
-->

### Context Manager

```python
from clipboard import Clipboard


with Clipboard() as clipboard:

    # Set Clipboard
    clipboard['text'] = 'Hello World!'
    # OR
    clipboard.set_clipboard('text') = 'Hello World!'

    # Get Clipboard
    text = clipboard['text']
    # OR
    text = clipboard.get_clipboard('text')
```

<!--

    # HTML
    clipboard['html'] = '<h1>Hello World</h1>'
-->

## See Clipboard Formats

`ClipboardFormats`
: Enum for clipboard formats.

`ClipboardFormats.CF_HTML`
: Represents HTML format.

```python
from clipboard import Clipboard
from clipboard import ClipboardFormats
from clipboard import HTMLClipboard
```
