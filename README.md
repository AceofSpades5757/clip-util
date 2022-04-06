[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# Description

Package for accessing the clipboard with Python.

# Installation

`pip install clip-util`

# Features

_Windows Only_

Allows for text and HTML on Windows.

## Supported Clipboard Formats

* Text
* HTML

# Usage

## Clipboard

Will open and close every time the values are set, or retrieved. It's better to use a context manager.

``` python
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

# HTML
clipboard['html'] = '<h1>Hello World</h1>'
```

### Context Manager

``` python
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

    # HTML
    clipboard['html'] = '<h1>Hello World</h1>'
```

## See Clipboard Formats

`ClipboardFormats`
: Enum for clipboard formats.

`ClipboardFormats.CF_HTML`
: Represents HTML format.

``` python
from clipboard import Clipboard
from clipboard import ClipboardFormats
from clipboard import HTMLClipboard
```
