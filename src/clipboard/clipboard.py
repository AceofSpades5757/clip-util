"""Clipboard module.

TODO: Make `get_clipboard`'s default to check available formats instead of just
using the default format.
FIXME: Copying using normal methods and then using `get_clipboard` doesn't work
properly. It gives a bunch of null bytes as a string.
FIXME: HTML_Format doesn't work for some reason. Fix this.
FIXME: Typing appears to be off.
    * There are a lot of parameters with a default of None that are not Optional.
    * There are some parameters typed as `int`, but they look like they should
    be `Optional[HANDLE]` instead.
"""

import ctypes
import logging
import os
from pathlib import Path
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
from clipboard.errors import EmptyClipboardError
from clipboard.errors import FormatNotSupportedError
from clipboard.errors import GetClipboardError
from clipboard.errors import LockError
from clipboard.errors import OpenClipboardError
from clipboard.errors import SetClipboardError
from clipboard.formats import ClipboardFormat
from clipboard.html_clipboard import HTMLTemplate


hMem = HANDLE  # Type Alias
GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040
GMEM_DDESHARE = 0x2000


logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
if os.environ.get("LOGLEVEL"):
    logger.setLevel(os.environ["LOGLEVEL"])

    file_handler = logging.FileHandler("clipboard.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_clipboard(format: Optional[Union[int, ClipboardFormat]] = None) -> Optional[Union[str, bytes]]:
    """Conveniency wrapper to get clipboard.

    Instead of using the `Clipboard.default_format`, this function uses the
    first available format on the clipboard.
    """
    if format is None:
        available = get_available_formats()
        if available:
            format = available[0]
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
    ) -> Optional[Union[str, bytes]]:
        """Get data from clipboard, returning None if nothing is on it.

        Raises
        ------
        FormatNotSupportedError
            If the format is not supported.
        GetClipboardError
            If getting the clipboard data failed.
        LockError
            If locking the clipboard failed.
            If unlocking the clipboard failed.
        """
        logger.info("Getting clipboard data")

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
        self.h_clip_mem: HANDLE = GetClipboardData(format)
        if self.h_clip_mem is None:
            raise GetClipboardError("The `GetClipboardData` function failed.")
        self.address = self._lock(self.h_clip_mem)  # type: ignore
        self.size = GlobalSize(self.address)
        if not self.size:
            # 0 means that the function failed.
            raise GetClipboardError("The `GlobalSize` function failed.")

        string: ctypes.Array[ctypes.c_byte]
        content: str
        if format == ClipboardFormat.CF_UNICODETEXT.value:
            string = (ctypes.c_byte * self.size).from_address(
                int(self.address)  # type: ignore
            )
            content = bytearray(string)[:-2].decode(encoding=UTF_ENCODING)
        elif (
            format == ClipboardFormat.CF_HTML.value
            or format == ClipboardFormat.HTML_Format.value
        ):
            bytes_ = (ctypes.c_char * self.size).from_address(
                int(self.address)  # type: ignore
            )
            content = bytes(bytes_).decode(HTML_ENCODING)[:-1]

        else:
            string = (ctypes.c_byte * self.size).from_address(
                int(self.address)  # type: ignore
            )
            try:
                content = bytearray(string)[:-1].decode(encoding="utf-8")
            except UnicodeDecodeError:
                return bytes(string)

        # FIXME: This fails frequently, likely due to a resource management
        # error.
        try:
            self._unlock()
        except LockError:
            pass
        return content

    def set_clipboard(
        self, content: str, format: Union[int, ClipboardFormat] = None
    ) -> HANDLE:
        """Set clipboard.

        Raises
        ------
        SetClipboardError
            If setting the clipboard data failed.
        """
        logger.info("Setting clipboard data")

        set_handle: HANDLE = self._set_clipboard(content, format)

        return set_handle

    def _set_clipboard(
        self, content: str, format: Union[int, ClipboardFormat] = None
    ) -> HANDLE:
        """Hides the HANDLE.

        Raises
        ------
        SetClipboardError
            If setting the clipboard data failed.
        OpenClipboardError
            If opening the clipboard failed.
            Can be raised if the clipboard isn't already opened.
        EmptyClipboardError
            If emptying the clipboard failed.
            Need to empty the clipboard each time before setting new data.
        FormatNotSupportedError
            If the format is not supported.
        """

        logger.info("_Setting clipboard data")

        if format is None:
            format = self.format

        if not self.opened:
            with self:
                return self._set_clipboard(content=content, format=format)

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
        ClipboardFormat object, return the respective integer.

        Raises
        ------
        FormatNotSupportedError
            If the format is not supported.
        """

        logger.info("Resolving clipboard format")

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
        """Get data from clipboard, returning None if nothing is on it.

        Raises
        ------
        FormatNotSupportedError
            If the format is not supported.
        GetClipboardError
            If getting the clipboard data failed.
        """
        return self.get_clipboard(format)

    def __setitem__(self, format, content) -> None:
        """Set clipboard content based on given format.

        Raises
        ------
        SetClipboardError
            If setting the clipboard data failed.
        FormatNotSupportedError
            If the given format is not supported.
        OpenClipboardError
            Can only be raised if the clipboard isn't already opened.
        EmptyClipboardError
            If emptying the clipboard failed.
            The clipboard needs to be emptied before setting new data.
        """
        format = self._resolve_format(format)
        self._empty()
        self.set_clipboard(content, format)

    def __enter__(self):
        """Open clipboard.

        Raises
        ------
        OpenClipboardError
            If opening the clipboard failed.
            Can only be raised if the clipboard isn't already opened.
        """
        logger.info("Entering context manager")

        # There is an issue with opening the clipboard repeatedly.
        # This is likely due to a logical error when locking and unlocking.
        #
        # This successfully fixes the issue, although it is blunt.
        max_tries = 3
        tries = 0
        while not self.opened and tries < max_tries:
            tries += 1
            if self._open():
                return self
            self._close()
        else:
            raise OpenClipboardError("Failed to open clipboard.")

    def __exit__(
        self, exception_type, exception_value, exception_traceback
    ) -> bool:
        logger.info("Exiting context manager")
        if exception_type is not None:
            import traceback

            traceback.print_exception(
                exception_type, exception_value, exception_traceback
            )

        self._close()
        return True

    def _open(self, handle: int = None) -> bool:
        logger.info("_Opening clipboard")
        opened: bool = bool(OpenClipboard(handle))
        self.opened = opened
        return opened

    def _close(self) -> bool:
        logger.info("_Closing clipboard")
        self.opened = False
        # FIXME: This fails frequently, likely due to a resource management
        # error.
        try:
            self._unlock()
        except LockError:
            pass
        return CloseClipboard()

    def _lock(self, handle: HANDLE) -> LPVOID:
        """Lock clipboard.

        Raises
        ------
        LockError
            If locking the clipboard failed.
        """
        logger.info("_Locking clipboard")
        locked: LPVOID = GlobalLock(handle)
        self.locked = bool(locked)
        if locked is None:
            raise LockError("The `GlobalLock` function failed.")

        return locked

    def _unlock(self, handle: HANDLE = None) -> bool:
        """Unlock clipboard.

        Raises
        ------
        LockError
            If unlocking the clipboard failed.
        """
        logger.info("_Unlocking clipboard")
        if handle is None:
            handle = self.h_clip_mem

        unlocked: bool = bool(GlobalUnlock(handle))  # non-zero
        self.locked = not unlocked
        if not unlocked:
            raise LockError("The `GlobalUnlock` function failed.")
        return unlocked

    def _empty(self) -> bool:
        """Empty clipboard.

        Raises
        ------
        EmptyClipboardError
            If emptying the clipboard failed.
        """
        logger.info("_Emptying clipboard")
        if not self.opened:
            with self:
                return self._empty()
        elif self.opened:
            # FIXME: A false means that this failed.
            return bool(EmptyClipboard())
        else:
            raise EmptyClipboardError("Emptying the clipboard failed.")
