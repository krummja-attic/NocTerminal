from __future__ import annotations
from time import time
from morphism import *
import nocterminal as noc

from .view import View


class TextInputView(View):

    def __init__(
            self,
            callback, initial_value="",
            color_unselected_fg=0xFFFFFFFF,
            color_unselected_bg=0xFF151515,
            color_selected_fg=0xFFFFFF00,
            color_selected_bg=0xFF151515,
            *args, **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self.text = initial_value
        self.callback = callback
        self.color_unselected_fg = color_unselected_fg
        self.color_unselected_bg = color_unselected_bg
        self.color_selected_fg = color_selected_fg
        self.color_selected_bg = color_selected_bg

    @property
    def intrinsic_size(self):
        return Size(len(self.text) + 1, 1)

    def draw(self, ctx):
        color_fg = self.color_selected_fg if self.is_first_responder else self.color_unselected_fg
        color_bg = self.color_selected_bg if self.is_first_responder else self.color_unselected_bg
        ctx.color = color_fg
        ctx.bkcolor = color_bg
        ctx.print(Point(0, 0), self.text)

        text_len = len(self.text)

        if int(self.bounds.width) > text_len:
            ctx.print(Point(text_len, 0), '.' * (self.bounds.width - text_len))

        if self.is_first_responder and int(time() * 1.2) % 2 == 0:
            ctx.put(Point(text_len, 0), "█")

    def debug_string(self):
        return super().debug_string() + ' ' + repr(self.text)

    def did_resign_first_responder(self):
        super().did_resign_first_responder()
        self.set_needs_layout()

    @property
    def can_become_first_responder(self):
        return True

    def _update_text(self, value):
        self.text = value
        self.superview.set_needs_layout()

    def terminal_read(self, val):
        if val == noc.terminal.TK_ENTER:
            self.callback(self.text)
            self.first_responder_container_view.find_next_responder()
            return True
        if val == noc.terminal.TK_TAB:
            self.callback(self.text)
            return False
        elif val == noc.terminal.TK_BACKSPACE:
            if self.text:
                self._update_text(self.text[:-1])
                return True
        elif noc.terminal.check(noc.terminal.TK_WCHAR):
            self._update_text(self.text + chr(noc.terminal_state.wchar))
            return True
