Features
========

*Windows Only*

Allows for text and HTML on Windows.

Supported Clipboard Formats
===========================

- Text
- HTML

Clipboard
=========

Will open and close every time the values are set, or retrieved. It's better to use a context manager.

.. code:: python
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

Context Manager
===============

.. code:: python
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

Get Clipboard Formats
=====================

``ClipboardFormats``
: Enum for clipboard formats.

``ClipboardFormats.CF_HTML``
: Represents HTML format.

``ClipboardFormats.CF_RTF``
: Represents rich text format.

..code:: python
  from clipboard import Clipboard
  from clipboard import ClipboardFormats
  from clipboard import HTMLClipboard
