from __future__ import annotations

from collections import deque
from contextlib import contextmanager
from nocterminal.blt.base_terminal import terminal, BaseTerminal
from nocterminal.blt.state import terminal_state
from morphism import *


LINE_STYLES = {
    'single':  {
        'T': '─',
        'B': '─',
        'L': '│',
        'R': '│',
        'TL': '┌',
        'TR': '┐',
        'BL': '└',
        'BR': '┘',
        },
    'double':  {
        'T': '═',
        'B': '═',
        'L': '║',
        'R': '║',
        'TL': '╔',
        'TR': '╗',
        'BL': '╚',
        'BR': '╝',
        },
    }


class Context(BaseTerminal):

    def __init__(self):
        self._offset = Point(0, 0)
        self._render_stack = deque([])
        self._crop_rect = None
        self._fg = terminal_state.color
        self._bg = terminal_state.bkcolor

    @property
    def state(self):
        return terminal_state

    @property
    def color(self):
        return self._fg

    @property
    def bkcolor(self):
        return self._bg

    @color.setter
    def color(self, value):
        self._fg = value
        terminal.color(value)

    @bkcolor.setter
    def bkcolor(self, value):
        self._bg = value
        terminal.bkcolor(value)

    @contextmanager
    def translate(self, offset: Point):
        """Translate all positional renderer calls by the given `offset` by
        using the following syntax:

            offset = Point(x, y)  # let x = 2, y = 2
            with RenderManager.translate(offset):
                RenderManager.put(Point(0, 0), '@')  # puts at (2, 2)
        """
        previous = self._offset
        self._offset = self._offset + offset
        yield
        self._offset = previous

    @staticmethod
    def has_input():
        return terminal.has_input()

    @staticmethod
    def refresh() -> None:
        return terminal.refresh()

    @staticmethod
    def setup(composition: bool = True, bkcolor: int = 0xFF151515) -> None:
        return terminal.setup(composition=composition, bkcolor=bkcolor)

    @staticmethod
    def teardown() -> None:
        return terminal.teardown()

    @staticmethod
    def layer(value: int):
        return terminal.layer(value)

    @staticmethod
    def clear(color=0xFFFFFFFF, bkcolor=0xFF151515) -> None:
        return terminal.clear(color, bkcolor)

    @staticmethod
    def read():
        return terminal.read()

    def clear_area(self, rect: Rect, *args) -> None:
        computed_rect = Rect(rect.origin + self._offset, rect.size)
        if self._crop_rect and not self._crop_rect.intersects(computed_rect):
            return
        return terminal.clear_area(computed_rect, *args)

    def crop(self, rect: Rect, *args) -> None:
        computed_rect = Rect(rect.origin + self._offset, rect.size)
        if self._crop_rect and not self._crop_rect.intersects(computed_rect):
            return
        return terminal.crop(computed_rect, *args)

    def put(self, point, char):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return terminal.put(computed_point, char)

    def print(self, point: Point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return terminal.puts(computed_point, *args)

    def print_big(self, point: Point, string: str):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        terminal.puts(computed_point, f"[font=title]{string}[/font]")

    def pick(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return terminal.pick(computed_point, *args)

    def pick_color(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return terminal.pick_color(computed_point, *args)

    def pick_bkcolor(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return terminal.pick_bkcolor(computed_point, *args)

    def put_ext(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return terminal.put_ext(computed_point, *args)

    def read_str(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return terminal.read_str(computed_point, *args)

    def fill_area(self, rect: Rect, char: str = "█", layer: int = 0, color: int = None) -> None:
        if color is None:
            color = self._bg
        terminal.layer(layer)
        terminal.color(color)
        for _x in range(int(rect.left), int(rect.right)):
            for _y in range(int(rect.top), int(rect.bottom)):
                terminal.put(Point(_x, _y), char)

    def draw_box(self, rect: Rect, ctx=None, style='single'):
        if ctx is None:
            ctx = self

        style = LINE_STYLES[style]

        for point in rect.points_top:
            ctx.put(point, style['T'])
        for point in rect.points_bottom:
            ctx.put(point, style['B'])
        for point in rect.points_left:
            ctx.put(point, style['L'])
        for point in rect.points_right:
            ctx.put(point, style['R'])
        ctx.put(rect.origin, style['TL'])
        ctx.put(rect.point_top_right, style['TR'])
        ctx.put(rect.point_bottom_left, style['BL'])
        ctx.put(rect.point_bottom_right, style['BR'])


context = Context()
