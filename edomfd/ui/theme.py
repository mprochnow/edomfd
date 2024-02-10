# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

# https://github.com/israel-dryer/ttk-arc-clone/blob/master/arc_theme_ttk.py
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk


PANEL_BACKGROUND = '#000000'
TEXT_COLOR = '#F0CE0B'
ENTRY_BACKGROUND = '#471A01'


def create_widget_styles(style: ttk.Style) -> None:
    style.configure('TFrame', background=PANEL_BACKGROUND)
    style.configure('Content.TFrame', background=ENTRY_BACKGROUND)

    style.configure('TLabel', background=TEXT_COLOR, foreground=PANEL_BACKGROUND, padding=(1, 0, 1, 1))
    style.map('TLabel', background=[('disabled', ENTRY_BACKGROUND)], foreground=[('disabled', TEXT_COLOR)])

    m = tkfont.nametofont("TkDefaultFont").metrics()
    y_max = m['ascent'] + m['descent'] + 4

    style.configure('Treeview', fieldbackground=PANEL_BACKGROUND, borderwidth=0, background=PANEL_BACKGROUND,
                    foreground=TEXT_COLOR, rowheight=y_max)
    style.configure('Treeview.Heading', background=ENTRY_BACKGROUND, foreground=TEXT_COLOR, relief=tk.FLAT)
    style.map('Treeview.Heading', background=[('active', ENTRY_BACKGROUND)])

    style.configure('TButton', background=ENTRY_BACKGROUND)


def apply_theme() -> None:
    style = ttk.Style()
    style.theme_create('edomfd', 'default')
    style.theme_use('edomfd')

    create_widget_styles(style)
