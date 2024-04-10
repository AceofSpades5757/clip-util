"""Clipboard module.

TODO: Make `get_clipboard`'s default to check available formats instead of just
using the default format.
FIXME: HTML_Format doesn't work for some reason. Fix this.
"""

import ctypes
import logging
from typing import List
from typing import Optional
from typing import Union

from clipboard._c_interface import HANDLE
from clipboard._c_interface import LPVOID
from clipboard._c_interface import CloseClipboard
from clipboard._c_interface import EmptyClipboard
from clipboard._c_interface import EnumClipboardFormats
from clipboard._c_interface import GetClipboardData
from clipboard._c_interface import GlobalAlloc
from clipboard._c_interface import GlobalLock
from clipboard._c_interface import GlobalSize
from clipboard._c_interface import GlobalUnlock
from clipboard._c_interface import OpenClipboard
from clipboard._c_interface import SetClipboardData
from clipboard.constants import HTML_ENCODING
from clipboard.constants import UTF_ENCODING
from clipboard.formats import ClipboardFormat
from clipboard.html_clipboard import HTMLTemplate
from clipboard.errors import EmptyClipboardError
from clipboard.errors import FormatNotSupportedError
from clipboard.errors import GetClipboardError
from clipboard.errors import OpenClipboardError
from clipboard.errors import SetClipboardError


hMem = HANDLE  # Type Alias
GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040
GMEM_DDESHARE = 0x2000


logger = logging.getLogger(__name__)


def get_clipboard(format: Union[int, ClipboardFormat] = None) -> Optional[str]:
    """Conveniency wrapper to get clipboard."""
    with Clipboard() as cb:
        return cb.get_clipboard(format=format)


def set_clipboard(
    content: str, format: Union[int, ClipboardFormat] = None
) -> None:
    """Conveniency wrapper to set clipboard."""
    with Clipboard() as cb:
        return cb.set_clipboard(content=content, format=format)


def get_available_formats() -> list[int]:
    """Conveniency wrapper to get available formats."""
    with Clipboard() as cb:
        return cb.available_formats()


class Clipboard:
    default_format: ClipboardFormat = ClipboardFormat.CF_UNICODETEXT

    def __init__(self, format: Union[ClipboardFormat, str, int] = None):
        if format is None:
            format = self.default_format.value
        else:
            format = self._resolve_format(format)

        self.format: int = format  # type: ignore
        self.h_clip_mem: Optional[HANDLE] = None
        self.address: Optional[LPVOID] = None
        self.size: Optional[int] = None  # in bytes

        self.locked: bool = False
        self.opened: bool = False

    def available_formats(self) -> List[int]:
        """Return all available clipboard formats on clipboard.

        First format is the format on the clipboard, depending on your system.
        """
        # TODO Add this to a base class (HTML clipboard could use this)

        logger.info("Getting available clipboard formats")

        def get_formats(formats: List = None) -> List[int]:
            if formats is None:
                formats = [EnumClipboardFormats(0)]

            last_format = formats[-1]
            if last_format == 0:
                return formats[:-1]
            else:
                return formats + [EnumClipboardFormats(last_format)]

        available_formats: List[int] = []
        if not self.opened:
            with self:
                available_formats = self.available_formats()
        elif self.opened:
            available_formats = get_formats()

        return available_formats

    def get_clipboard(
        self, format: Union[int, ClipboardFormat] = None
    ) -> Optional[str]:
        """Get data from clipboard, returning None if nothing is on it."""

        if not self.opened:
            with self:
                return self.get_clipboard(format=format)

        if format is None:
            format = self.format
        else:
            format = self._resolve_format(format)

        formats = self.available_formats()
        if format not in formats:
            raise FormatNotSupportedError(
                f"{format} is not supported for getting the clipboard. Choose from following {formats}"
            )

        # Info
        self.h_clip_mem = GetClipboardData(format)
        self.address = self._lock(self.h_clip_mem)  # type: ignore
        self.size = GlobalSize(self.address)

        if not self.size:
            raise GetClipboardError("Getting the global size failed.")

        string: ctypes.Array[ctypes.c_byte]
        text: str
        if format == ClipboardFormat.CF_UNICODETEXT.value:
            string = (ctypes.c_byte * self.size).from_address(
                int(self.address)  # type: ignore
            )
            text = bytearray(string).decode(encoding=UTF_ENCODING)[:-1]

            return text
        elif (
            format == ClipboardFormat.CF_HTML.value
            or format == ClipboardFormat.HTML_Format.value
        ):
            bytes_ = (ctypes.c_char * self.size).from_address(
                int(self.address)  # type: ignore
            )
            html = bytes(bytes_).decode(HTML_ENCODING)[:-1]

            return html

        else:
            string = (ctypes.c_byte * self.size).from_address(
                int(self.address)  # type: ignore
            )
            text = bytearray(string).decode(encoding="utf-8")[:-1]

            return text

    def set_clipboard(
        self, content: str, format: Union[int, ClipboardFormat] = None
    ) -> HANDLE:
        """Set clipboard."""

        set_handle: HANDLE = self._set_clipboard(content, format)

        return set_handle

    def _set_clipboard(
        self, content: str, format: Union[int, ClipboardFormat] = None
    ) -> HANDLE:
        """Hides the HANDLE."""

        if format is None:
            format = self.format

        if not self.opened:
            with self:
                return self._set_clipboard(content=content, format=format)

        if format is None:
            format = self.format
        format = self._resolve_format(format)
        self._empty()

        set_handle: HANDLE
        alloc_handle: HANDLE
        content_bytes: bytes
        contents_ptr: LPVOID
        if format == ClipboardFormat.CF_UNICODETEXT.value:
            content_bytes = content.encode(encoding="utf-16le")

            alloc_handle = GlobalAlloc(
                GMEM_MOVEABLE | GMEM_ZEROINIT, len(content_bytes) + 2
            )
            contents_ptr = GlobalLock(alloc_handle)
            ctypes.memmove(contents_ptr, content_bytes, len(content_bytes))
            GlobalUnlock(alloc_handle)

            set_handle = SetClipboardData(format, alloc_handle)

        elif (
            format == ClipboardFormat.CF_HTML.value
            or format == ClipboardFormat.HTML_Format.value
        ):
            template: HTMLTemplate = HTMLTemplate(content)
            html_content_bytes: bytes = template.generate().encode(
                encoding=HTML_ENCODING
            )

            alloc_handle = GlobalAlloc(
                GMEM_MOVEABLE | GMEM_ZEROINIT, len(html_content_bytes) + 1
            )
            contents_ptr = GlobalLock(alloc_handle)  # type: ignore
            ctypes.memmove(
                contents_ptr, html_content_bytes, len(html_content_bytes)
            )
            GlobalUnlock(alloc_handle)

            set_handle = SetClipboardData(format, alloc_handle)
        else:
            content_bytes = content.encode(encoding="utf-8")

            alloc_handle = GlobalAlloc(GMEM_MOVEABLE, len(content_bytes) + 1)
            contents_ptr = GlobalLock(alloc_handle)
            ctypes.memmove(contents_ptr, content_bytes, len(content_bytes))
            GlobalUnlock(alloc_handle)

            set_handle = SetClipboardData(format, alloc_handle)

        if set_handle is None:
            raise SetClipboardError("Setting the clipboard failed.")

        return set_handle

    def _resolve_format(self, format: Union[ClipboardFormat, str, int]) -> int:
        """Given an integer, respresenting a clipboard format, or a
        ClipboardFormat object, return the respective integer."""

        if isinstance(format, ClipboardFormat):
            format = format.value
        elif isinstance(format, int):
            pass
        elif isinstance(format, str):
            try:
                format = ClipboardFormat[format].value
            except KeyError:
                formats = self.available_formats()
                raise FormatNotSupportedError(
                    f"{format} is not a supported clipboard format."
                    f" Choose from following {formats}"
                )

        # FIXME: There are issues with HTML_Format, so use CF_HTML
        if format == ClipboardFormat.HTML_Format.value:
            format = ClipboardFormat.CF_HTML.value
        return format  # type: ignore

    def __getitem__(self, format: Union[int, ClipboardFormat] = None):
        return self.get_clipboard(format)

    def __setitem__(self, format, content) -> None:
        format = self._resolve_format(format)
        self._empty()
        self.set_clipboard(content, format)

    def __enter__(self):
        if self._open():
            return self
        else:
            raise OpenClipboardError("Failed to open clipboard.")

    def __exit__(
        self, exception_type, exception_value, exception_traceback
    ) -> bool:
        if exception_type is not None:
            import traceback

            traceback.print_exception(
                exception_type, exception_value, exception_traceback
            )

        self._close()
        return True

    def _open(self, handle: int = None) -> bool:
        self.opened = True
        return OpenClipboard(handle)

    def _close(self) -> bool:
        self.opened = False
        self._unlock()
        return CloseClipboard()

    def _lock(self, handle: HANDLE) -> LPVOID:
        self.locked = True
        # if fails, GlobalLock returns NULL (False in Python)
        return GlobalLock(handle)

    def _unlock(self, handle: HANDLE = None) -> int:
        if handle is None:
            handle = self.h_clip_mem

        self.locked = False
        return GlobalUnlock(handle)

    def _empty(self) -> int:
        if not self.opened:
            with self:
                return self._empty()
        elif self.opened:
            return_code = EmptyClipboard()
        else:
            raise EmptyClipboardError("Emptying the clipboard failed.")

        return return_code
