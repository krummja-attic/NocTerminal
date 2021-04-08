from __future__ import annotations
from morphism import Size
from .first_responder import FirstResponderContainerView
from nocterminal.blt.state import terminal_state


class Screen:

    name: str

    def __init__(self) -> None:
        self._director = None
        self._terminal_readers = []
        self.covers_screen: bool = True

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, value):
        self._director = value

    def add_terminal_reader(self, reader):
        if not getattr(reader, 'terminal_read'):
            raise ValueError("Invalid reader")
        self._terminal_readers.append(reader)

    def remove_terminal_reader(self, reader):
        self._terminal_readers.remove(reader)

    def on_enter(self, *args):
        pass

    def on_leave(self, *args):
        pass

    def become_active(self):
        pass

    def resign_active(self):
        pass

    def terminal_update(self, is_active=False):
        return True

    def terminal_read(self, char):
        for reader in self._terminal_readers:
            reader.terminal_read(char)
        return True


class UIScreen(Screen):

    def __init__(self, views):
        super().__init__()
        if not isinstance(views, list):
            views = [views]
        self.view = FirstResponderContainerView(subviews=views, screen=self)
        self.add_terminal_reader(self.view)

    def terminal_read(self, val):
        super().terminal_read(val)

    # noinspection PyUnresolvedReferences
    def terminal_update(self, is_active=False):
        ctx = self._director.context
        ctx.bkcolor = 0xFF151515
        ctx.color = 0xFFFFFFFF
        self.view.frame = self.view.frame.with_size(
            Size(terminal_state.width, terminal_state.height))
        self.view.perform_layout()
        self.view.perform_draw(ctx)
        ctx.bkcolor = 0xFF151515
        ctx.color = 0xFFFFFFFF
        return True
