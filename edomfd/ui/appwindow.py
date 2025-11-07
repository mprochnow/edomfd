# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import tkinter as tk
from tkinter import ttk

import screeninfo

import edoevent
import edostate
from ui import theme
from ui.onfootpanel import OnFootPanel
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
        self._root.bind('<Escape>', self._close)
        self._root.bind('<F11>', self._toggle_fullscreen)

        self._frame = ttk.Frame(self._root)
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)
        self._frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self._ship_panel: ShipPanel = ShipPanel(self._frame)
        self._ship_panel_visible: bool = False
        self._on_foot_panel: OnFootPanel = OnFootPanel(self._frame)
        self._on_foot_panel_visible: bool = False

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

    def set_current_system(self, system_name: str) -> None:
        self._ship_panel.set_current_system(system_name)

    def set_route(self, nav_route: list[edostate.RouteEntry]) -> None:
        self._ship_panel.set_route(nav_route)

    def set_cargo(self, cargo_used: int, cargo_capacity: int, cargo_list: list[edostate.CargoListEntry]) -> None:
        self._ship_panel.set_cargo(cargo_used, cargo_capacity, cargo_list)

    def show_landing_pad(self, show: bool, landing_pad: int | None) -> None:
        self._ship_panel.show_landing_pad_panel(show, landing_pad)

    def show_ship_panel(self) -> None:
        self._ship_panel.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self._ship_panel_visible = True

        self._on_foot_panel.grid_forget()
        self._on_foot_panel_visible = False

    def show_on_foot_panel(self) -> None:
        self._ship_panel.grid_forget()
        self._ship_panel_visible = False

        self._on_foot_panel.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self._on_foot_panel_visible = True

    def set_status(self, status: edoevent.Status) -> None:
        if self._on_foot_panel_visible:
            self._on_foot_panel.set_status(status)
        else:
            self._ship_panel.set_status(status)
