""" Helper to interface with the C code.

Note: This did not feel like a simple process to identify the paths to access
the C functions.
"""
import ctypes
from ctypes.wintypes import BOOL
from ctypes.wintypes import HANDLE
from ctypes.wintypes import HGLOBAL
from ctypes.wintypes import HWND
from ctypes.wintypes import LPSTR
from ctypes.wintypes import LPVOID
from ctypes.wintypes import LPWSTR
from ctypes.wintypes import UINT


# C Libraries
windll = ctypes.windll  # type: ignore
user32 = windll.user32
kernel32 = windll.kernel32

# C Functions
OpenClipboard = user32.OpenClipboard
OpenClipboard.argtypes = [HWND]
OpenClipboard.restype = BOOL

CloseClipboard = user32.CloseClipboard
CloseClipboard.argtypes = []
CloseClipboard.restype = BOOL

SetClipboardData = user32.SetClipboardData
SetClipboardData.argtypes = [UINT, HANDLE]
SetClipboardData.restype = HANDLE

EmptyClipboard = user32.EmptyClipboard
EmptyClipboard.argtypes = []
EmptyClipboard.restype = BOOL

GetClipboardData = user32.GetClipboardData
GetClipboardData.argtypes = [UINT]
GetClipboardData.restype = HANDLE


IsClipboardFormatAvailable = user32.IsClipboardFormatAvailable
IsClipboardFormatAvailable.argtypes = [UINT]
IsClipboardFormatAvailable.restype = BOOL

# Returns first available clipboard format in a specified list
GetPriorityClipboardFormat = user32.GetPriorityClipboardFormat
GetPriorityClipboardFormat.argtypes = [UINT, ctypes.c_int]
GetPriorityClipboardFormat.restype = ctypes.c_int

# w - unicode (utf-16 on windows)
# a - ansi
GetClipboardFormatNameA = user32.GetClipboardFormatNameA
GetClipboardFormatNameA.argtypes = [UINT, LPSTR, ctypes.c_int]
GetClipboardFormatNameA.restype = ctypes.c_int

GetClipboardFormatNameW = user32.GetClipboardFormatNameW
GetClipboardFormatNameW.argtypes = [UINT, LPWSTR, ctypes.c_int]
GetClipboardFormatNameW.restype = ctypes.c_int

GlobalLock = kernel32.GlobalLock
GlobalLock.argtypes = [HGLOBAL]
GlobalLock.restype = LPVOID

GlobalUnlock = kernel32.GlobalUnlock
GlobalUnlock.argtypes = [HGLOBAL]
GlobalUnlock.restype = BOOL

GlobalSize = kernel32.GlobalSize
GlobalSize.argtypes = [HGLOBAL]
GlobalSize.restype = int  # SIZE_T

GlobalAlloc = kernel32.GlobalAlloc
GlobalAlloc.argtypes = [UINT, ctypes.c_int]
GlobalAlloc.restype = HANDLE


EnumClipboardFormats = user32.EnumClipboardFormats
EnumClipboardFormats.argtypes = [UINT]
EnumClipboardFormats.restype = UINT


# Additional
CF_HTML = ctypes.windll.user32.RegisterClipboardFormatA('HTML Format')  # type: ignore
