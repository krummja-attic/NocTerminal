from __future__ import annotations
import time
import nocterminal as noc
from nocterminal.ui import Screen
from nocterminal.blt import context
from typing import *

from nocterminal.core_loop import CoreLoop

if TYPE_CHECKING:
    from nocterminal.blt.context import Context


class Director(CoreLoop):

    def __init__(self, client=None) -> None:
        super().__init__()
        self._stack: List[Screen] = []
        self._should_continue: bool = True
        self.client = client
        self.context: Context = context

    @property
    def active_screen(self) -> Optional[Screen]:
        if self._stack:
            return self._stack[-1]
        else:
            return None

    def replace_screen(self, screen: Screen):
        if self._stack:
            self.pop_screen(may_exit=False)
        self.push_screen(screen)

    def push_screen(self, screen: Screen):
        if self.active_screen:
            self.active_screen.resign_active()
        self._stack.append(screen)
        screen.director = self
        screen.on_enter()
        screen.become_active()

    def pop_screen(self, may_exit=True):
        if self.active_screen:
            self.active_screen.resign_active()
        if self._stack:
            last_screen = self._stack.pop()
            last_screen.on_leave()
        if self.active_screen:
            self.active_screen.become_active()
        elif may_exit:
            self._should_continue = False

    def pop_to_first_screen(self):
        while len(self._stack) > 1:
            self.pop_screen()

    def get_initial_screen(self):
        raise NotImplementedError()

    def quit(self):
        while self._stack:
            self.pop_screen(may_exit=True)

    def start(self):
        self.replace_screen(self.get_initial_screen())
        noc.terminal.setup()
        self.main_loop()
        noc.terminal.teardown()

    def main_loop(self) -> None:
        try:
            iteration = False
            while self.loop_iteration():
                iteration = True
            if not iteration:
                print("Exited after a single cycle.")
        except KeyboardInterrupt:
            pass

    def loop_iteration(self) -> bool:
        if self.context.has_input():
            char = self.context.read()
            self.terminal_read(char)

        i = 0
        for j, screen in enumerate(self._stack):
            if screen.covers_screen:
                i = j
        for screen in self._stack[i:]:
            screen.terminal_update(screen == self._stack[-1])

        self.context.refresh()
        return self._should_continue

    def terminal_read(self, char):
        if self._stack:
            self.active_screen.terminal_read(char)
