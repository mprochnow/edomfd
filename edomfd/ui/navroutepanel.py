import tkinter as tk
from tkinter import ttk

import edostate


class NavRoutePanel(ttk.Frame):
    def __init__(self, parent, **kwargs) -> None:
        self._set_styles()

        kwargs['style'] = 'NavRoute.TFrame'
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._tree = ttk.Treeview(self, show="headings", columns=('system', 'star_class', 'distance'),
                                  selectmode='none', style='NavRoute.Treeview')
        self._tree.grid(column=0, row=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self._tree.heading('system', text="System", anchor=tk.W)
        self._tree.heading('star_class', text="Star Class", anchor=tk.W)
        self._tree.heading('distance', text="Distance", anchor=tk.W)

    def set(self, nav_route: list[edostate.RouteEntry]) -> None:
        self._tree.delete(*self._tree.get_children())

        for entry in nav_route:
            if not self._tree.exists(entry.system_address):
                self._tree.insert('', tk.END, iid=entry.system_address,
                                  values=(entry.star_system, entry.star_class, f"{entry.distance:.1f}Ly"))

    def _set_styles(self) -> None:
        self._style = ttk.Style()
        self._style.configure('NavRoute.TFrame', background='#000000', borderwith=0)

        self._style.configure('NavRoute.Treeview', fieldbackground='#000000', borderwidth=0, background='#000000',
                              foreground='#DE9A01')
        self._style.configure('NavRoute.Treeview.Heading', background='#000000', foreground='#DE9A01',
                              relief=tk.FLAT)
        self._style.map('NavRoute.Treeview.Heading', background=[('active', '#000000')])
