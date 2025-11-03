import tkinter as tk
from tkinter import ttk


class OnFootPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        label = ttk.Label(self, text="In Station")
        label.grid(row=0, column=0, sticky=tk.W + tk.E)
        self._label_in_station = ttk.Label(self, text="-")
        self._label_in_station.grid(row=0, column=1, sticky=tk.W + tk.E)

        label = ttk.Label(self, text="In Hangar")
        label.grid(row=1, column=0, sticky=tk.W + tk.E)
        self._label_in_hangar = ttk.Label(self, text="-")
        self._label_in_hangar.grid(row=1, column=1, sticky=tk.W + tk.E)

        label = ttk.Label(self, text="In Social Space")
        label.grid(row=2, column=0, sticky=tk.W + tk.E)
        self._label_in_social_space = ttk.Label(self, text="-")
        self._label_in_social_space.grid(row=2, column=1, sticky=tk.W + tk.E)

        label = ttk.Label(self, text="Exterior")
        label.grid(row=3, column=0, sticky=tk.W + tk.E)
        self._label_exterior = ttk.Label(self, text="-")
        self._label_exterior.grid(row=3, column=1, sticky=tk.W + tk.E)

        label = ttk.Label(self, text="On Planet")
        label.grid(row=4, column=0, sticky=tk.W + tk.E)
        self._label_on_planet = ttk.Label(self, text="-")
        self._label_on_planet.grid(row=4, column=1, sticky=tk.W + tk.E)

        label = ttk.Label(self, text="Geo Coordinates")
        label.grid(row=5, column=0, sticky=tk.W + tk.E)
        self._label_geo_coords = ttk.Label(self, text="-")
        self._label_geo_coords.grid(row=5, column=1, sticky=tk.W + tk.E)

        label = ttk.Label(self, text="Heading")
        label.grid(row=6, column=0, sticky=tk.W + tk.E)
        self._label_heading = ttk.Label(self, text="-")
        self._label_heading.grid(row=6, column=1, sticky=tk.W + tk.E)


    def set_status(self, in_station: bool, in_hangar: bool, in_social_space: bool, exterior: bool, on_planet: bool,
                   geo_coords: tuple[float | None, float | None], heading: float | None) -> None:
        self._label_in_station.configure(text=f"{int(in_station)}")
        self._label_in_hangar.configure(text=f"{int(in_hangar)}")
        self._label_in_social_space.configure(text=f"{int(in_social_space)}")
        self._label_exterior.configure(text=f"{int(exterior)}")
        self._label_on_planet.configure(text=f"{int(on_planet)}")
        self._label_geo_coords.configure(text=f"{geo_coords[0]:.6f}, {geo_coords[1]:.6f}" if geo_coords[0] else "-")
        self._label_heading.configure(text=f"{heading:.6f}" if heading else "-")
