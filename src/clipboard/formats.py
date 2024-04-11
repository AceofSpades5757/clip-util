import ctypes
from enum import Enum
from enum import EnumMeta
from typing import Any
from typing import List
from typing import Optional

from clipboard._c_interface import CF_HTML
from clipboard._c_interface import CF_RTF
from clipboard._c_interface import EnumClipboardFormats
from clipboard._c_interface import GetClipboardFormatNameA


class ExtendedEnum(EnumMeta):
    def __contains__(cls, item: Any):
        return any(
            [
                item in cls.names,  # type: ignore
                item in cls.values,  # type: ignore
                item in ClipboardFormat.__members__.values(),
            ]
        )


class ClipboardFormat(Enum, metaclass=ExtendedEnum):
    CF_TEXT = 1
    CF_UNICODETEXT = 13
    CF_LOCALE = 16

    CF_HTML = CF_HTML
    CF_RTF = CF_RTF
    HTML_Format = 49418

    text = CF_UNICODETEXT  # alias
    html = HTML_Format  # alias
    HTML = html  # alias
    rtf = CF_RTF  # alias

    @classmethod  # type: ignore
    @property
    def values(cls):
        return [i.value for i in cls]

    @classmethod  # type: ignore
    @property
    def names(cls):
        return [i.name for i in cls]

    def __str__(self):
        return f"{str(self.value)} {str(self.name)}"

    def __eq__(self, other):
        if isinstance(self, type(other)):
            return self.name == other.name and self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return False


def get_clipboard_formats(formats: List[int] = None) -> List[int]:
    """Return all available clipboard formats on clipboard.

    First format is the format on the clipboard, depending on your system.
    """
    if formats is None:
        formats = [EnumClipboardFormats(0)]

    last_format: int = formats[-1]
    if last_format == 0:
        return formats[:-1]
    else:
        return formats + [EnumClipboardFormats(last_format)]


def get_format_name(format_code: int) -> Optional[str]:
    """Get the name of the format by it's number.

    C function does not work for standard types (e.g. 1 for CF_TEXT).
    So, this function will use ClipboardFormat for those in the standard.

    Returns
    -------
    str, optional
        The name of the format.
        None if the format is not found.
    """
    # Built-In
    if format_code in ClipboardFormat.values:  # type: ignore
        return ClipboardFormat(format_code).name

    buffer_size = 256
    buffer = ctypes.create_string_buffer(buffer_size)
    return_code = GetClipboardFormatNameA(
        format_code,
        buffer,
        buffer_size,
    )

    # Failed
    if return_code == 0:
        last_error: int = ctypes.get_last_error()
        if last_error == 0:
            # No Error
            return None
        if last_error == 87:
            # This indicates that the first parameter is not a valid clipboard format.
            return None
        error = ctypes.WinError(last_error)
        raise error

    # ansii string
    format_name: str = buffer.value.decode("utf-8")

    return format_name
