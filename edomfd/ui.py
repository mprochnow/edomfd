from pprint import pprint
from tkinter import *
from tkinter import ttk

import screeninfo


class AppWindow:
    def __init__(self, monitors: list[screeninfo.Monitor]):
        self._fullscreen: bool = False

        self._tk: Tk = Tk()
        self._tk.title("EDO MFD")

        self._monitors = monitors

        # self._frame = Frame(self._tk)

        self._tk.bind('<Escape>', self._close)
        self._tk.bind('<F11>', self._toggle_fullscreen)
        self._tk.bind('<Configure>', self._on_configure)

        self._maybe_move_to_secondary_monitor()

    def show(self):
        self._tk.mainloop()

    def _maybe_move_to_secondary_monitor(self):
        for monitor in self._monitors:
            if not monitor.is_primary:
                self._tk.geometry(f"+{monitor.x:+}{monitor.y:+}")
                self._toggle_fullscreen()
                break

    def _close(self, event=None):
        self._tk.quit()

    def _toggle_fullscreen(self, event=None):
        self._fullscreen = not self._fullscreen

        if self._fullscreen:
            self._geometry = self._tk.geometry()
            # Tk.attribute("-fullscreen", True) always moves app window to the primary monitor.
            # This is a work-around for this behavior.
            self._tk.state('zoomed')
            self._tk.overrideredirect(True)
        else:
            self._tk.state('normal')
            self._tk.geometry(self._geometry)
            self._tk.overrideredirect(False)

    def _on_configure(self, event=None):
        pass
