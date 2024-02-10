# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import tkinter as tk
from tkinter import ttk


class StatusPanel(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1, uniform='foobar')
        self.columnconfigure(1, weight=1, uniform='foobar')
        self.columnconfigure(2, weight=1, uniform='foobar')
        self.columnconfigure(3, weight=1, uniform='foobar')
        self.columnconfigure(4, weight=1, uniform='foobar')
        self.columnconfigure(5, weight=1, uniform='foobar')

        self._label_mass_locked = ttk.Label(self, text="MASS LOCKED")
        self._label_mass_locked.configure(state='disabled', anchor=tk.CENTER)
        self._label_mass_locked.grid(column=0, row=0, padx=1, pady=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self._label_landing_gear = ttk.Label(self, text="LANDING GEAR")
        self._label_landing_gear.configure(state='disabled', anchor=tk.CENTER)
        self._label_landing_gear.grid(column=1, row=0, padx=1, pady=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self._label_cargo_scoop = ttk.Label(self, text="CARGO SCOOP")
        self._label_cargo_scoop.configure(state='disabled', anchor=tk.CENTER)
        self._label_cargo_scoop.grid(column=2, row=0, padx=1, pady=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self._label_hardpoints = ttk.Label(self, text="HARDPOINTS")
        self._label_hardpoints.configure(state='disabled', anchor=tk.CENTER)
        self._label_hardpoints.grid(column=3, row=0, padx=1, pady=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self._label_lights = ttk.Label(self, text="LIGHTS")
        self._label_lights.configure(state='disabled', anchor=tk.CENTER)
        self._label_lights.grid(column=4, row=0, padx=1, pady=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self._label_night_vision = ttk.Label(self, text="NIGHT VISION")
        self._label_night_vision.configure(state='disabled', anchor=tk.CENTER)
        self._label_night_vision.grid(column=5, row=0, padx=1, pady=1, sticky=tk.N + tk.E + tk.S + tk.W)

    def set(self, mass_locked: bool, cargo_scoop_deployed: bool, landing_gear: bool, hardpoints: bool,
            lights: bool, night_vision: bool) -> None:
        self._label_mass_locked.configure(state='enabled' if mass_locked else 'disabled')
        self._label_landing_gear.configure(state='enabled' if landing_gear else 'disabled')
        self._label_hardpoints.configure(state='enabled' if hardpoints else 'disabled')
        self._label_lights.configure(state='enabled' if lights else 'disabled')
        self._label_night_vision.configure(state='enabled' if night_vision else 'disabled')
        self._label_cargo_scoop.configure(state='enabled' if cargo_scoop_deployed else 'disabled')
