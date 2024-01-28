import tkinter as tk
from tkinter import ttk


class BountyPanel(ttk.Frame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)

        self._label_bounty = ttk.Label(self, text="Bounty: 0 Cr")
        self._label_bounty.configure(state='disabled')
        self._label_bounty.grid(column=0, row=0, pady=1, sticky=tk.N+tk.E+tk.S+tk.W)

    def set(self, bounty: int) -> None:
        self._label_bounty.configure(text=f"Bounty: {bounty:,} Cr")
