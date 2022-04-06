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

## Set Clipboard

``` python
from clipboard import Clipboard


with Clipboard() as clipboard:

    # Set Clipboard
    clipboard['text'] = 'Hello World!'

    # Get Clipboard
    text = clipboard['text']
```

<!-- BUG
clipboard = Clipboard()

clipboard['txt'] = 'Hello There.'
clipboard['html'] = '<h1>Hello World</h1>'

clipboard.set_clipboard('Hey?')
data: str = clipboard.get_clipboard()
-->

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
