import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

from edostate import CargoListEntry
from ui import theme


class CargoPanel(ttk.Frame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        font = tkfont.nametofont("TkDefaultFont")

        self._label_cargo_capacity = ttk.Label(self, text="Cargo: -/-")
        self._label_cargo_capacity.configure(state='disabled')
        self._label_cargo_capacity.grid(column=0, row=0, pady=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self._tree = ttk.Treeview(self, show="headings", columns=('name', 'count'),
                                  selectmode='none', style='NavRoute.Treeview')
        self._tree.grid(column=0, row=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self._tree.tag_configure('entry', background=theme.ENTRY_BACKGROUND)
        self._tree.heading('name', text="Name", anchor=tk.W)

        column_width = font.measure('0000 ')
        self._tree.heading('count', text="Qty", anchor=tk.W)
        self._tree.column('count', width=column_width, stretch=False)

    def set(self, cargo_used: int, cargo_capacity: int, cargo_list: list[CargoListEntry]) -> None:
        self._tree.delete(*self._tree.get_children())

        for entry in cargo_list:
            self._tree.insert('', tk.END, tags='entry', values=(entry.name, f"{entry.count}"))

        self._label_cargo_capacity.configure(text=f"Cargo: {cargo_used}/{cargo_capacity}")
