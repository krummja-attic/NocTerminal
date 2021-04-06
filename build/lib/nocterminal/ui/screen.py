from __future__ import annotations
from morphism import Size
from .first_responder import FirstResponderContainerView


class AbstractScreen:

    name: str

    def __init__(self, director) -> None:
        self._director = director
        self._terminal_readers = []
        self.covers_screen: bool = True

    @property
    def director(self):
        return self._director

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


class UIScreen(AbstractScreen):

    def __init__(self, views, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(views, list):
            views = [views]
        self.view = FirstResponderContainerView(subviews=views, screen=self)
        self.add_terminal_reader(self.view)

    def terminal_read(self, val):
        super().terminal_read(val)

    # noinspection PyUnresolvedReferences
    def terminal_update(self, is_active=False):
        ctx = self.game.renderer
        ctx.bkcolor = 0xFF151515
        self.view.frame = self.view.frame.with_size(
            Size(Options.SCREEN_WIDTH, Options.SCREEN_HEIGHT))
        self.view.perform_layout()
        self.view.perform_draw(ctx)
        ctx.bkcolor = 0xFF151515