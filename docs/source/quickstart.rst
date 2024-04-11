Features
========

*Windows Only*

Allows for text and HTML on Windows.

Supported Clipboard Formats
===========================

- Text
- HTML
- RTF

Clipboard
=========

Will open and close every time the values are set, or retrieved. It's better to use a context manager.

.. code:: python

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

Context Manager
===============

.. code:: python

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

Get Clipboard Formats
=====================

``ClipboardFormats``
: Enum for clipboard formats.

``ClipboardFormats.CF_HTML``
: Represents HTML format.

``ClipboardFormats.CF_RTF``
: Represents rich text format.

.. code:: python

    from clipboard import Clipboard
    from clipboard import ClipboardFormat


    with Clipboard() as clipboard:

        # Get All Available Formats
        format_ids: list[int] = clipboard.available_formats()

        # Get Specific Format by ID
        # Use parentheses to access the format
        formats: list[ClipboardFormat] = []
        for format_id in format_ids:
            if format_id in ClipboardFormat:
                format: ClipboardFormat = ClipboardFormat(format_id)
                formats.append(format)
            else:
                # Format is not supported directly by this library
                pass

        # Get Specified Format by Name
        # Use bracket notation to access the format
        format_name: str
        for format_name in [f.name for f in formats]:
            if format_name in ClipboardFormat:
                format: ClipboardFormat = ClipboardFormat[format_name]
                name: str = format.name
            else:
                # Format is not supported directly by this library
                pass

