# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import tkinter as tk
from tkinter import ttk

import screeninfo

from ui import theme
from ui.cargopanel import CargoPanel
from ui.landingpadpanel import LandingPadPanel
from ui.navroutepanel import NavRoutePanel
from ui.statuspanel import StatusPanel


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

        self._frame = ttk.Frame(self._root)
        self._frame.columnconfigure(0, weight=1, uniform="fubar")
        self._frame.columnconfigure(1, weight=1, uniform="fubar")

        self._frame.rowconfigure(0, weight=1)
        self._frame.rowconfigure(1, weight=0)
        self._frame.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

        self.landing_pad_panel: LandingPadPanel = LandingPadPanel(self._frame)

        self.nav_route_panel: NavRoutePanel = NavRoutePanel(self._frame)
        self.nav_route_panel.grid(column=0, row=0, padx=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.cargo_panel: CargoPanel = CargoPanel(self._frame)
        self.cargo_panel.grid(column=1, row=0, padx=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.status_panel: StatusPanel = StatusPanel(self._frame)
        self.status_panel.grid(column=0, row=1, pady=0, columnspan=2, sticky=tk.N+tk.E+tk.S+tk.W)

        self._root.bind('<Escape>', self._close)
        self._root.bind('<F11>', self._toggle_fullscreen)

        self._maybe_move_to_secondary_monitor()

    def show(self):
        self._root.mainloop()

    def destroy(self, _=None):
        self._root.destroy()

    def show_landing_pad_panel(self, show: bool) -> None:
        if show:
            self.landing_pad_panel.grid(column=0, row=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
            self.nav_route_panel.grid_forget()
            self.cargo_panel.grid_forget()
        else:
            self.landing_pad_panel.grid_forget()
            self.nav_route_panel.grid(column=0, row=0, padx=1, sticky=tk.N+tk.E+tk.S+tk.W)
            self.cargo_panel.grid(column=1, row=0, padx=1, sticky=tk.N+tk.E+tk.S+tk.W)

    def _maybe_move_to_secondary_monitor(self):
        for monitor in self._monitors:
            if not monitor.is_primary:
                self._root.geometry(f"+{monitor.x:+}{monitor.y:+}")
                self._toggle_fullscreen()
                break

    def _close(self, _=None):
        self._root.quit()

    def _toggle_fullscreen(self, _=None):
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
