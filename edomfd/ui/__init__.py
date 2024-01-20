import tkinter as tk
from tkinter import ttk

import screeninfo

from ui.geocoordinatespanel import GeoCoordinatesPanel
from ui.statuspanel import StatusPanel

QUEUE_CHECK_TIME = 100  # ms


class AppWindow:
    def __init__(self, monitors: list[screeninfo.Monitor]):
        self._monitors: list[screeninfo.Monitor] = monitors

        self._fullscreen: bool = False

        self.tk = tk.Tk()
        self.tk.title("EDO MFD")
        self.tk.columnconfigure(0, weight=1)
        self.tk.rowconfigure(0, weight=1)

        self._style = ttk.Style()
        self._style.configure('TFrame', background='#DE9A01')

        self._frame = ttk.Frame(self.tk)
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=0)
        self._frame.rowconfigure(1, weight=1)
        self._frame.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

        self.status_panel: StatusPanel = StatusPanel(self._frame)
        self.status_panel.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

        self.geocoordinates_panel: GeoCoordinatesPanel = GeoCoordinatesPanel(self._frame)
        self.geocoordinates_panel.grid(column=0, row=1, pady=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.tk.bind('<Escape>', self._close)
        self.tk.bind('<F11>', self._toggle_fullscreen)

        self._maybe_move_to_secondary_monitor()

    def show(self):
        self.tk.mainloop()

    def destroy(self):
        self.tk.destroy()

    def _maybe_move_to_secondary_monitor(self):
        for monitor in self._monitors:
            if not monitor.is_primary:
                self.tk.geometry(f"+{monitor.x:+}{monitor.y:+}")
                self._toggle_fullscreen()
                break

    def _close(self, event=None):
        self.tk.quit()

    def _toggle_fullscreen(self, event=None):
        self._fullscreen = not self._fullscreen

        if self._fullscreen:
            self.tk.update_idletasks()
            self._geometry = self.tk.geometry()
            # Tk.attribute("-fullscreen", True) always moves app window to the primary monitor.
            # This is a work-around for this behavior.
            self.tk.state('zoomed')
            self.tk.overrideredirect(True)
        else:
            self.tk.state('normal')
            self.tk.geometry(self._geometry)
            self.tk.overrideredirect(False)
