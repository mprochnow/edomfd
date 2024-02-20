# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

# https://github.com/israel-dryer/ttk-arc-clone/blob/master/arc_theme_ttk.py
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk


COLOR_PANEL_BACKGROUND = '#131313'
COLOR_TEXT = '#ff8e00'
COLOR_ENTRY_BACKGROUND = '#312412'
COLOR_TEXT2 = '#08baff'
COLOR_WARNING = '#b80300'


def create_widget_styles(style: ttk.Style) -> None:
    style.configure('TFrame', background=COLOR_PANEL_BACKGROUND)
    style.configure('Content.TFrame', background=COLOR_ENTRY_BACKGROUND)

    style.configure('TLabel', background=COLOR_TEXT, foreground=COLOR_PANEL_BACKGROUND, padding=(1, 0, 1, 1))
    style.map('TLabel', background=[('disabled', COLOR_ENTRY_BACKGROUND)], foreground=[('disabled', COLOR_TEXT)])

    m = tkfont.nametofont("TkDefaultFont").metrics()
    y_max = m['ascent'] + m['descent'] + 4

    style.configure('Treeview', fieldbackground=COLOR_PANEL_BACKGROUND, borderwidth=0,
                    background=COLOR_PANEL_BACKGROUND, foreground=COLOR_TEXT, rowheight=y_max)
    style.configure('Treeview.Heading', background=COLOR_ENTRY_BACKGROUND, foreground=COLOR_TEXT, relief=tk.FLAT)
    style.map('Treeview.Heading', background=[('active', COLOR_ENTRY_BACKGROUND)])

    style.configure('TButton', background=COLOR_ENTRY_BACKGROUND)


def apply_theme() -> None:
    style = ttk.Style()
    style.theme_create('edomfd', 'default')
    style.theme_use('edomfd')

    create_widget_styles(style)
