# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import tkinter as tk

import screeninfo

from ui import theme
from ui.shippanel import ShipPanel


class AppWindow:
    def __init__(self, monitors: list[screeninfo.Monitor], root: tk.Tk):
        self._monitors: list[screeninfo.Monitor] = monitors

        self._fullscreen: bool = False

        self._root = root
        theme.apply_theme()
        self._root.title("EDO MFD")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._context_menu = tk.Menu(self._root, tearoff=0)
        self._context_menu.add_command(label="Quit", command=self.destroy)

        self._root.bind('<3>', lambda e: self._context_menu.post(e.x_root, e.y_root))

        self.ship_panel = ShipPanel(self._root)
        self.ship_panel.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self._root.bind('<Escape>', self._close)
        self._root.bind('<F11>', self._toggle_fullscreen)

        self._maybe_move_to_secondary_monitor()

    def show(self) -> None:
        self._root.mainloop()

    def destroy(self, _=None) -> None:
        self._root.destroy()

    def _maybe_move_to_secondary_monitor(self) -> None:
        for monitor in self._monitors:
            if not monitor.is_primary:
                self._root.geometry(f"+{monitor.x:+}{monitor.y:+}")
                self._toggle_fullscreen()
                break

    def _close(self, _=None) -> None:
        self._root.quit()

    def _toggle_fullscreen(self, _=None) -> None:
        self._fullscreen = not self._fullscreen

        if self._fullscreen:
            self._root.update_idletasks()
            self._geometry = self._root.geometry()
            # Tk.attribute("-fullscreen", True) always moves app window to the primary monitor.
            # This is a work-around for this behavior.
            self._root.state('zoomed')
            self._root.overrideredirect(True)
        else:
            self._root.state('normal')
            self._root.geometry(self._geometry)
            self._root.overrideredirect(False)
