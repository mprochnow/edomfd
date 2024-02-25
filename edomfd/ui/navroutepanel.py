# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

import edostate
from ui import theme, fa


class NavRoutePanel(ttk.Frame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self._parent = parent
        self._system_name = ''

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        font = tkfont.nametofont("TkDefaultFont")

        self._frame = ttk.Frame(self, style='Content.TFrame')
        self._frame.grid(column=0, row=0, pady=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self._frame.columnconfigure(0, weight=0)
        self._frame.columnconfigure(1, weight=0)

        self._label_star_system = ttk.Label(self._frame, text="-")
        self._label_star_system.configure(state='disabled')
        self._label_star_system.grid(column=0, row=0, sticky=tk.N+tk.S+tk.W)

        fm = tkfont.nametofont("TkDefaultFont").metrics()

        self._copy_icon = fa.icon.get_tk_icon('copy', fa.Style.REGULAR, fm['ascent'] - fm['descent'], theme.COLOR_TEXT)
        self._copy_button = ttk.Button(self._frame, image=self._copy_icon, command=self._copy_system_name_to_clipboard)
        self._copy_button.grid(column=1, row=0, sticky=tk.N+tk.S)

        self._tree = ttk.Treeview(self, show="headings", columns=('system', 'star_class', 'distance'),
                                  selectmode='none', style='NavRoute.Treeview')
        self._tree.grid(column=0, row=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self._tree.tag_configure('entry', background=theme.COLOR_ENTRY_BACKGROUND)
        self._tree.heading('system', text="System", anchor=tk.W)

        column_width = font.measure('Class ')
        self._tree.heading('star_class', text="Class", anchor=tk.W)
        self._tree.column('star_class', minwidth=column_width, width=column_width, stretch=False)

        column_width = font.measure('Distance ')
        self._tree.heading('distance', text="Distance", anchor=tk.W)
        self._tree.column('distance', minwidth=column_width, width=column_width, stretch=False)

    def set_current_system(self, name: str) -> None:
        self._system_name = name
        self._label_star_system.configure(text=f"{name}")

    def set_route(self, nav_route: list[edostate.RouteEntry]) -> None:
        self._tree.delete(*self._tree.get_children())

        for entry in nav_route:
            self._tree.insert('', tk.END, tags='entry',
                              values=(entry.star_system, entry.star_class, f"{entry.distance:.1f}Ly"))

    def _copy_system_name_to_clipboard(self):
        self._parent.clipboard_clear()
        self._parent.clipboard_append(self._system_name)
