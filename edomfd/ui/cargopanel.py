import tkinter as tk
from tkinter import ttk


class CargoPanel(ttk.Frame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)

        self._label_cargo_capacity = ttk.Label(self, text="Cargo: -/-")
        self._label_cargo_capacity.configure(state='disabled')
        self._label_cargo_capacity.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

    def set(self, cargo_used: int, cargo_capacity: int) -> None:
        self._label_cargo_capacity.configure(text=f"Cargo: {cargo_used}/{cargo_capacity}")
