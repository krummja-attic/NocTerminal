from __future__ import annotations

from collections import deque
from contextlib import contextmanager
from nocterminal.blt.base_terminal import BaseTerminal
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
        super().__init__()
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
        super().color(value)

    @bkcolor.setter
    def bkcolor(self, value):
        self._bg = value
        super().bkcolor(value)

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

    def has_input(self):
        return super().has_input()

    def refresh(self) -> None:
        return super().refresh()

    def setup(self, composition=True, bkcolor=0xFF151515) -> None:
        return super().setup(composition=composition, bkcolor=bkcolor)

    def teardown(self) -> None:
        return super().teardown()

    def push_to_stack(self, func):
        self._render_stack.append(func)

    def clear_stack(self):
        self._render_stack.clear()

    def update(self) -> None:
        while len(self._render_stack) > 0:
            draw = self._render_stack.popleft()
            draw(0)
        self.clear_stack()
        self.refresh()

    def layer(self, value: int):
        return super().layer(value)

    def clear(self, bkcolor=0xFF151515) -> None:
        return super().clear(bkcolor)

    def clear_area(self, rect: Rect, *args) -> None:
        computed_rect = Rect(rect.origin + self._offset, rect.size)
        if self._crop_rect and not self._crop_rect.intersects(computed_rect):
            return
        return super().clear_area(computed_rect, *args)

    def crop(self, rect: Rect, *args) -> None:
        computed_rect = Rect(rect.origin + self._offset, rect.size)
        if self._crop_rect and not self._crop_rect.intersects(computed_rect):
            return
        return super().crop(computed_rect, *args)

    def put(self, point, char):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return super().put(computed_point, char)

    def print(self, point: Point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return super().puts(computed_point, *args)

    def print_big(self, point: Point, string: str):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        self.terminal.puts(computed_point, f"[font=title]{string}[/font]")

    def pick(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return super().pick(computed_point, *args)

    def pick_color(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return super().pick_color(computed_point, *args)

    def pick_bkcolor(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return super().pick_bkcolor(computed_point, *args)

    def put_ext(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return super().put_ext(computed_point, *args)

    def read_str(self, point, *args):
        computed_point = point + self._offset
        if self._crop_rect and computed_point not in self._crop_rect:
            return
        return super().read_str(computed_point, *args)

    def fill_area(self, rect: Rect, char: str = "█", layer: int = 0, color: int = None) -> None:
        if color is None:
            color = self._bg
        super().layer(layer)
        super().color(color)
        for _x in range(int(rect.left), int(rect.right)):
            for _y in range(int(rect.top), int(rect.bottom)):
                super().put(Point(_x, _y), char)

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
