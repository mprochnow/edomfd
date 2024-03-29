# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import tkinter as tk
from tkinter import ttk


class GeoCoordinatesPanel(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self._label_latitude = ttk.Label(self, text="Latitude: -")
        self._label_latitude.configure(state='disabled')
        self._label_latitude.grid(column=0, row=0, padx=0, pady=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self._label_heading = ttk.Label(self, text="Heading: -")
        self._label_heading.configure(state='disabled')
        self._label_heading.grid(column=1, row=0, padx=0, pady=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self._label_longitude = ttk.Label(self, text="Longitude: -")
        self._label_longitude.configure(state='disabled')
        self._label_longitude.grid(column=0, row=1, padx=0, pady=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self._label_altitude = ttk.Label(self, text="Altitude: -")
        self._label_altitude.configure(state='disabled')
        self._label_altitude.grid(column=1, row=1, padx=0, pady=0, sticky=tk.N + tk.E + tk.S + tk.W)

    def set(self, latitude: float | None, longitude: float | None, heading: int | None, altitude: int | None) -> None:
        self._label_latitude.configure(text="Latitude: " + f"{latitude if latitude else '-'}")
        self._label_longitude.configure(text="Longitude: " + f"{longitude if longitude else '-'}")

        if heading:
            heading_text = f"Heading: {heading}°"
        else:
            heading_text = "Heading: -"
        self._label_heading.configure(text=heading_text)

        if altitude:
            if altitude > 100000:
                altitude_text = f"Altitude: {altitude // 1000}km"
            elif altitude > 10000:
                altitude_text = f"Altitude: {altitude / 1000:.1f}km"
            elif altitude > 1000:
                altitude_text = f"Altitude: {altitude / 1000:.2f}km"
            else:
                altitude_text = f"Altitude: {altitude}m"
        else:
            altitude_text = "Altitude: -"
        self._label_altitude.configure(text=altitude_text)
