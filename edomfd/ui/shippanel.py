import tkinter as tk
from tkinter import ttk

import edostate
from ui.cargopanel import CargoPanel
from ui.landingpadpanel import LandingPadPanel
from ui.navroutepanel import NavRoutePanel
from ui.statuspanel import StatusPanel


class ShipPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1, uniform="fubar")
        self.columnconfigure(1, weight=1, uniform="fubar")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self._landing_pad_panel: LandingPadPanel = LandingPadPanel(self)

        self._nav_route_panel: NavRoutePanel = NavRoutePanel(self)
        self._nav_route_panel.grid(column=0, row=0, padx=1, sticky=tk.N + tk.E + tk.S + tk.W)

        self._cargo_panel: CargoPanel = CargoPanel(self)
        self._cargo_panel.grid(column=1, row=0, padx=1, sticky=tk.N + tk.E + tk.S + tk.W)

        self._status_panel: StatusPanel = StatusPanel(self)
        self._status_panel.grid(column=0, row=1, pady=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

    def set_status(self, mass_locked: bool, cargo_scoop_deployed: bool, landing_gear: bool, hardpoints: bool,
            lights: bool, night_vision: bool) -> None:
        self._status_panel.set(mass_locked, cargo_scoop_deployed, landing_gear, hardpoints, lights, night_vision)

    def show_landing_pad_panel(self, show: bool, landing_pad: int | None = None) -> None:
        if show:
            self._landing_pad_panel.highlight_pad(landing_pad)
            self._landing_pad_panel.grid(column=0, row=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
            self._nav_route_panel.grid_forget()
            self._cargo_panel.grid_forget()
        else:
            self._landing_pad_panel.highlight_pad(None)
            self._landing_pad_panel.grid_forget()
            self._nav_route_panel.grid(column=0, row=0, padx=1, sticky=tk.N + tk.E + tk.S + tk.W)
            self._cargo_panel.grid(column=1, row=0, padx=1, sticky=tk.N + tk.E + tk.S + tk.W)

    def set_current_system(self, name: str) -> None:
        self._nav_route_panel.set_current_system(name)

    def set_route(self, nav_route: list[edostate.RouteEntry]) -> None:
        self._nav_route_panel.set_route(nav_route)

    def set_cargo(self, cargo_used: int, cargo_capacity: int, cargo_list: list[edostate.CargoListEntry]) -> None:
        self._cargo_panel.set(cargo_used, cargo_capacity, cargo_list)
