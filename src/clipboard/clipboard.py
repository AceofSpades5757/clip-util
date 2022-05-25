import ctypes
from typing import List
from typing import Optional
from typing import Union

from clipboard._c_interface import CloseClipboard
from clipboard._c_interface import EmptyClipboard
from clipboard._c_interface import EnumClipboardFormats
from clipboard._c_interface import GetClipboardData
from clipboard._c_interface import GlobalAlloc
from clipboard._c_interface import GlobalLock
from clipboard._c_interface import GlobalSize
from clipboard._c_interface import GlobalUnlock
from clipboard._c_interface import HANDLE
from clipboard._c_interface import LPVOID
from clipboard._c_interface import OpenClipboard
from clipboard._c_interface import SetClipboardData
from clipboard._logging import get_logger
from clipboard.constants import HTML_ENCODING
from clipboard.constants import UTF_ENCODING
from clipboard.formats import ClipboardFormat


hMem = HANDLE  # Type Alias
logger = get_logger(__name__)


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


class Clipboard:

    default_format: ClipboardFormat = ClipboardFormat.CF_UNICODETEXT

    def __init__(self, format: Union[ClipboardFormat, str, int] = None):

        if format is None:
            format = self.default_format.value
        else:
            format = self._resolve_format(format)

        self.format: int = format  # type: ignore
        # TODO Add type annotations
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

        logger.info("Getting available clipboard formats...")

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

        if format not in self.available_formats():
            formats = self.available_formats()
            message = (
                f"{format} not supported. Choose from following...\n"
                + "\n".join(map(str, formats))
            )
            raise Exception(message)

        # Info
        self.h_clip_mem = GetClipboardData(format)
        self.address = self._lock(self.h_clip_mem)  # type: ignore
        self.size = GlobalSize(self.address)

        if not self.size:
            raise Exception("Get Clipboard failed...")

        if format == ClipboardFormat.CF_UNICODETEXT.value:

            string: ctypes.Array[ctypes.c_byte] = (
                ctypes.c_byte * self.size
            ).from_address(
                int(self.address)  # type: ignore
            )
            text: str = bytearray(string).decode(encoding=UTF_ENCODING)[:-1]

            return text
        elif (
            format == ClipboardFormat.CF_HTML.value
            or format == ClipboardFormat.HTML_Format.value
        ):

            bytes_ = (ctypes.c_char * self.size).from_address(
                int(self.address)  # type: ignore
            )
            html = bytes(bytes_).decode(HTML_ENCODING)

            return html

        else:
            return None

    def set_clipboard(
        self, content: str, format: Union[int, ClipboardFormat] = None
    ) -> None:
        """Set clipboard."""

        _: HANDLE = self._set_clipboard(content, format)

        return None

    def _set_clipboard(
        self, content: str, format: Union[int, ClipboardFormat] = None
    ) -> HANDLE:
        """Hides the HANDLE."""

        if format is None:
            format = self.default_format

        if not self.opened:
            with self:
                return self._set_clipboard(content=content, format=format)

        if format is None:
            format = self.format
        format = self._resolve_format(format)
        self._empty()

        set_handle: HANDLE
        alloc_handle: HANDLE
        if format == ClipboardFormat.CF_UNICODETEXT.value:

            # GMEM_DDESHARE = 0x2000
            GMEM_MOVEABLE = 0x0002
            GMEM_ZEROINIT = 0x0040

            # Needs a special encoding...
            content_bytes: bytes = content.encode(encoding="utf-16le")

            alloc_handle = GlobalAlloc(
                GMEM_MOVEABLE | GMEM_ZEROINIT, len(content_bytes) + 2
            )
            pcontents: LPVOID = GlobalLock(alloc_handle)
            ctypes.memmove(pcontents, content_bytes, len(content_bytes))
            GlobalUnlock(alloc_handle)

            set_handle = SetClipboardData(format, alloc_handle)

        elif (
            format == ClipboardFormat.CF_HTML.value
            or format == ClipboardFormat.HTML_Format.value
        ):
            # GMEM_DDESHARE = 0x2000
            GMEM_MOVEABLE = 0x0002
            GMEM_ZEROINIT = 0x0040

            # Needs a special encoding...
            html_content_bytes: bytes = content.encode(encoding="utf-16le")

            alloc_handle = GlobalAlloc(
                GMEM_MOVEABLE | GMEM_ZEROINIT, len(content) + 2
            )
            pcontents: LPVOID = GlobalLock(alloc_handle)  # type: ignore
            ctypes.memmove(pcontents, html_content_bytes, len(content))
            GlobalUnlock(alloc_handle)

            set_handle = SetClipboardData(format, alloc_handle)
        else:
            raise Exception(
                f"{format} not supported for setting to clipboard."
            )

        if set_handle is False:
            # handle will be set to NULL
            raise Exception("Set Clipboard failed...")

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
                # Not a Supported Format
                raise ValueError(
                    f"{format} is not a valid format. Choose from following...\n"
                    + "\n".join(map(str, ClipboardFormat))
                )

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
            raise Exception("Unable to open clipboard.")

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

    def _close(self) -> None:

        self.opened = False
        self._unlock()
        CloseClipboard()

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
            raise RuntimeError("Failed to empty clipboard.")

        return return_code
