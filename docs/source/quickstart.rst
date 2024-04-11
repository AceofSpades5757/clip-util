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

Get All Supported Formats
=====================

You can even get the content of all available formats currently in the clipboard.

.. code:: python

    from clipboard import get_available_formats
    from clipboard import get_format_name
    from clipboard import get_clipboard


    available: list[int] = get_available_formats()
    print(f"{available=}")

    for format_id in available:
        name: str = get_format_name(format_id)
        content: str = get_clipboard(format_id)
        print(f"{format_id=}", f"{name=}, {content=}")
