# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import math
import tkinter as tk
from tkinter import ttk

from ui.theme import COLOR_PANEL_BACKGROUND, COLOR_TEXT, COLOR_ENTRY_BACKGROUND, COLOR_TEXT2

BLINK_INTERVAL = 500
MARGIN = 20
LIGHTS_DIA = 4
LANDING_PAD_COUNT = 45


class LandingPadPanel(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._canvas = tk.Canvas(self, bg=COLOR_PANEL_BACKGROUND, bd=0, highlightthickness=0, relief='ridge')
        self._canvas.grid(column=0, row=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self._pads: list[int | None] = [None] * LANDING_PAD_COUNT
        self._left_circle1: int | None = None
        self._left_circle2: int | None = None

        self._blink_on = False
        self._highlighted_pad: int | None = None

        self.bind('<Configure>', self._on_configure)

    def highlight_pad(self, pad: int | None) -> None:
        if pad is None:
            if self._highlighted_pad is not None:
                self._canvas.itemconfig(self._pads[self._highlighted_pad - 1], fill=COLOR_ENTRY_BACKGROUND)
        else:
            self.after(BLINK_INTERVAL, self._blink)

        self._highlighted_pad = pad

    def _blink(self) -> None:
        if self._blink_on:
            circle_fill = COLOR_TEXT
            pad_fill = COLOR_TEXT2
        else:
            circle_fill = ''
            pad_fill = COLOR_ENTRY_BACKGROUND

        self._canvas.itemconfig(self._left_circle1, fill=circle_fill)
        self._canvas.itemconfig(self._left_circle2, fill=circle_fill)

        if self._highlighted_pad is not None:
            self._canvas.itemconfig(self._pads[self._highlighted_pad - 1], fill=pad_fill)

        self._blink_on = not self._blink_on

        if self._highlighted_pad is not None:
            self.after(BLINK_INTERVAL, self._blink)

    def _on_configure(self, event: tk.Event) -> None:
        self._canvas.delete('all')
        self._draw(event.width, event.height)

    def _draw(self, w: int, h: int) -> None:
        outline = COLOR_TEXT
        fill = COLOR_ENTRY_BACKGROUND

        r = min(w, h) // 2 - MARGIN

        r1 = self._get_points(r, w, h)
        r2 = self._get_points(r / 6 * 5, w, h)
        r3 = self._get_points(r / 6 * 4, w, h)
        r4 = self._get_points(r / 6 * 3, w, h)
        r5 = self._get_points(r / 6 * 2, w, h)
        r6 = self._get_points(r / 6, w, h)

        self._left_circle1 = self._draw_circle(r1[8][0] - MARGIN / 2, r1[8][1] + MARGIN / 2, LIGHTS_DIA)
        self._left_circle2 = self._draw_circle(r1[9][0] - MARGIN / 2, r1[9][1] - MARGIN / 2, LIGHTS_DIA)

        self._draw_circle(r1[3][0] + MARGIN / 2, r1[3][1] + MARGIN / 2, LIGHTS_DIA)
        self._draw_circle(r1[2][0] + MARGIN / 2, r1[2][1] - MARGIN / 2, LIGHTS_DIA)

        self._draw_landing_pads(r1, r2, r3, r4, r5, r6, outline, fill)

    def _draw_landing_pads(
            self,
            r1: list[tuple[float, float]],
            r2: list[tuple[float, float]],
            r3: list[tuple[float, float]],
            r4: list[tuple[float, float]],
            r5: list[tuple[float, float]],
            r6: list[tuple[float, float]],
            outline: str,
            fill: str
    ) -> None:
        self._canvas.create_polygon(*r1, outline=outline, fill=fill)

        self._pads[0] = self._canvas.create_polygon(r2[0], r1[0], r1[11], r2[11], outline=outline, fill=fill)
        self._pads[1] = self._canvas.create_polygon(r3[0], r2[0], r2[11], r3[11], outline=outline, fill=fill)
        self._pads[2] = self._canvas.create_polygon(r5[0], r4[0], r4[11], r5[11], outline=outline, fill=fill)
        self._pads[3] = self._canvas.create_polygon(r6[0], r5[0], r5[11], r6[11], outline=outline, fill=fill)

        self._pads[4] = self._canvas.create_polygon(r2[11], r1[11], r1[10], r2[10], outline=outline, fill=fill)
        self._pads[5] = self._canvas.create_polygon(r3[11], r2[11], r2[10], r3[10], outline=outline, fill=fill)
        self._pads[6] = self._canvas.create_polygon(r4[11], r3[11], r3[10], r4[10], outline=outline, fill=fill)
        self._pads[7] = self._canvas.create_polygon(r6[11], r4[11], r4[10], r6[10], outline=outline, fill=fill)

        self._pads[8] = self._canvas.create_polygon(r3[10], r1[10], r1[9], r3[9], outline=outline, fill=fill)
        self._pads[9] = self._canvas.create_polygon(r6[10], r4[10], r4[9], r6[9], outline=outline, fill=fill)

        self._pads[10] = self._canvas.create_polygon(r2[9], r1[9], r1[8], r2[8], outline=outline, fill=fill)
        self._pads[11] = self._canvas.create_polygon(r3[9], r2[9], r2[8], r3[8], outline=outline, fill=fill)
        self._pads[12] = self._canvas.create_polygon(r4[9], r3[9], r3[8], r4[8], outline=outline, fill=fill)
        self._pads[13] = self._canvas.create_polygon(r5[9], r4[9], r4[8], r5[8], outline=outline, fill=fill)
        self._pads[14] = self._canvas.create_polygon(r6[9], r5[9], r5[8], r6[8], outline=outline, fill=fill)

        self._pads[15] = self._canvas.create_polygon(r2[8], r1[8], r1[7], r2[7], outline=outline, fill=fill)
        self._pads[16] = self._canvas.create_polygon(r3[8], r2[8], r2[7], r3[7], outline=outline, fill=fill)
        self._pads[17] = self._canvas.create_polygon(r5[8], r4[8], r4[7], r5[7], outline=outline, fill=fill)
        self._pads[18] = self._canvas.create_polygon(r6[8], r5[8], r5[7], r6[7], outline=outline, fill=fill)

        self._pads[19] = self._canvas.create_polygon(r2[7], r1[7], r1[6], r2[6], outline=outline, fill=fill)
        self._pads[20] = self._canvas.create_polygon(r3[7], r2[7], r2[6], r3[6], outline=outline, fill=fill)
        self._pads[21] = self._canvas.create_polygon(r4[7], r3[7], r3[6], r4[6], outline=outline, fill=fill)
        self._pads[22] = self._canvas.create_polygon(r6[7], r4[7], r4[6], r6[6], outline=outline, fill=fill)

        self._pads[23] = self._canvas.create_polygon(r3[6], r1[6], r1[5], r3[5], outline=outline, fill=fill)
        self._pads[24] = self._canvas.create_polygon(r6[6], r4[6], r4[5], r6[5], outline=outline, fill=fill)

        self._pads[25] = self._canvas.create_polygon(r2[5], r1[5], r1[4], r2[4], outline=outline, fill=fill)
        self._pads[26] = self._canvas.create_polygon(r3[5], r2[5], r2[4], r3[4], outline=outline, fill=fill)
        self._pads[27] = self._canvas.create_polygon(r4[5], r3[5], r3[4], r4[4], outline=outline, fill=fill)
        self._pads[28] = self._canvas.create_polygon(r5[5], r4[5], r4[4], r5[4], outline=outline, fill=fill)
        self._pads[29] = self._canvas.create_polygon(r6[5], r5[5], r5[4], r6[4], outline=outline, fill=fill)

        self._pads[30] = self._canvas.create_polygon(r2[4], r1[4], r1[3], r2[3], outline=outline, fill=fill)
        self._pads[31] = self._canvas.create_polygon(r3[4], r2[4], r2[3], r3[3], outline=outline, fill=fill)
        self._pads[32] = self._canvas.create_polygon(r5[4], r4[4], r4[3], r5[3], outline=outline, fill=fill)
        self._pads[33] = self._canvas.create_polygon(r6[4], r5[4], r5[3], r6[3], outline=outline, fill=fill)

        self._pads[34] = self._canvas.create_polygon(r2[3], r1[3], r1[2], r2[2], outline=outline, fill=fill)
        self._pads[35] = self._canvas.create_polygon(r3[3], r2[3], r2[2], r3[2], outline=outline, fill=fill)
        self._pads[36] = self._canvas.create_polygon(r4[3], r3[3], r3[2], r4[2], outline=outline, fill=fill)
        self._pads[37] = self._canvas.create_polygon(r6[3], r4[3], r4[2], r6[2], outline=outline, fill=fill)

        self._pads[38] = self._canvas.create_polygon(r3[2], r1[2], r1[1], r3[1], outline=outline, fill=fill)
        self._pads[39] = self._canvas.create_polygon(r6[2], r4[2], r4[1], r6[1], outline=outline, fill=fill)

        self._pads[40] = self._canvas.create_polygon(r2[1], r1[1], r1[0], r2[0], outline=outline, fill=fill)
        self._pads[41] = self._canvas.create_polygon(r3[1], r2[1], r2[0], r3[0], outline=outline, fill=fill)
        self._pads[42] = self._canvas.create_polygon(r4[1], r3[1], r3[0], r4[0], outline=outline, fill=fill)
        self._pads[43] = self._canvas.create_polygon(r5[1], r4[1], r4[0], r5[0], outline=outline, fill=fill)
        self._pads[44] = self._canvas.create_polygon(r6[1], r5[1], r5[0], r6[0], outline=outline, fill=fill)

    def _draw_circle(self, x: float, y: float, r: float) -> int:
        return self._canvas.create_oval(x - r, y - r, x + r, y + r, outline=COLOR_TEXT, fill=COLOR_TEXT)

    @staticmethod
    def _get_points(r: float, w: float, h: float) -> list[tuple[float, float]]:
        points: list[tuple] = []

        for i in range(6):
            a = math.radians(15 + i * 30)

            points.append((r * math.sin(a), r * math.cos(a)))

        return [(w / 2 + p[0], h / 2 + p[1]) for p in points] + [(w / 2 - p[0], h / 2 - p[1]) for p in points]
