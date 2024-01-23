import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

import edostate
from ui import theme


class NavRoutePanel(ttk.Frame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        font = tkfont.nametofont("TkDefaultFont")

        self._tree = ttk.Treeview(self, show="headings", columns=('system', 'star_class', 'distance'),
                                  selectmode='none', style='NavRoute.Treeview')
        self._tree.grid(column=0, row=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self._tree.tag_configure('entry', background=theme.ENTRY_BACKGROUND)
        self._tree.heading('system', text="System", anchor=tk.W)

        column_width = font.measure('Star Class ')
        self._tree.heading('star_class', text="Star Class", anchor=tk.W)
        self._tree.column('star_class', minwidth=column_width, width=column_width, stretch=False)

        column_width = font.measure('Distance ')
        self._tree.heading('distance', text="Distance", anchor=tk.W)
        self._tree.column('distance', minwidth=column_width, width=column_width, stretch=False)

    def set(self, nav_route: list[edostate.RouteEntry]) -> None:
        self._tree.delete(*self._tree.get_children())

        for entry in nav_route:
            self._tree.insert('', tk.END, tags='entry',
                              values=(entry.star_system, entry.star_class, f"{entry.distance:.1f}Ly"))
