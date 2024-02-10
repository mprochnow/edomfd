# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import enum
import os.path

from PIL import Image, ImageDraw, ImageFont, ImageTk
from PIL.ImageFont import FreeTypeFont
from PIL.ImageTk import PhotoImage

from fa.meta import meta


class Style(enum.StrEnum):
    REGULAR = "regular"
    SOLID = "solid"
    BRANDS = "brands"


FONTS_DIR = 'otfs'
FONTS = {
    Style.REGULAR: 'Font Awesome 6 Free-Regular-400.otf',
    Style.SOLID: 'Font Awesome 6 Free-Solid-900.otf',
    Style.BRANDS: 'Font Awesome 6 Brands-Regular-400.otf'
}


class Icon:
    def __init__(self) -> None:
        self._font_cache: dict[(Style, int), FreeTypeFont] = {}

    def get_icon(self, name: str, style: Style, font_size: int, fg="black", bg=(0, 0, 0, 0)) -> Image:
        icon_meta = meta.get(name)
        assert icon_meta is not None, f"Icon with name '{name}' not found"
        assert style in icon_meta['styles'], f"Icon 'name' with style 'style' not found"

        icon_font: FreeTypeFont = self._get_font(style, font_size)
        icon_symbol: str = icon_meta['unicode']

        w, h = int(icon_font.getlength(icon_symbol)), font_size

        icon_image = Image.new('RGBA', (w, h), bg)

        draw = ImageDraw.Draw(icon_image)
        draw.text((w/2, h/2), icon_symbol, fg, icon_font, 'mm')

        return icon_image

    def get_tk_icon(self, name: str, style: Style, font_size: int, fg="black", bg=(0, 0, 0, 0)) -> PhotoImage:
        return ImageTk.PhotoImage(self.get_icon(name, style, font_size, fg, bg))

    def _get_font(self, style: Style, font_size: int) -> FreeTypeFont:
        font_id = (style, font_size)

        try:
            return self._font_cache[font_id]
        except KeyError:
            font_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), FONTS_DIR, FONTS[style])
            ttf = ImageFont.truetype(font_filename, font_size, encoding='unic')
            self._font_cache[font_id] = ttf

            return ttf


icon = Icon()
