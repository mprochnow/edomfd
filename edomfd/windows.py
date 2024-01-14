import ctypes
import uuid
from ctypes.wintypes import DWORD, HANDLE

# https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid
FOLDERID_SavedGames = uuid.UUID('{4C5C32FF-BB9D-43b0-B5B4-2D72E54EAAA4}')

SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
SHGetKnownFolderPath.argtypes = [ctypes.c_char_p, DWORD, HANDLE, ctypes.POINTER(ctypes.c_wchar_p)]

CoTaskMemFree = ctypes.windll.ole32.CoTaskMemFree
CoTaskMemFree.argtypes = [ctypes.c_void_p]


def get_known_folder_path(guid: uuid.UUID) -> str | None:
    """Wrapper for Windows function SHGetKnownFolderPath"""
    buf = ctypes.c_wchar_p()  # Pointer to buffer
    if SHGetKnownFolderPath(ctypes.create_string_buffer(guid.bytes_le), 0, 0, ctypes.byref(buf)):
        return None
    result = buf.value  # Copy data from buffer
    CoTaskMemFree(buf)  # Free buffer
    return result
