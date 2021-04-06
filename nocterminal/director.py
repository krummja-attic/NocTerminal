from __future__ import annotations
from nocterminal.ui import Screen
from nocterminal.blt import Context
from typing import *

from nocterminal.core_loop import CoreLoop


class Director(CoreLoop):

    def __init__(self) -> None:
        super().__init__()
        self._stack: List[Screen] = []
        self._should_exit: bool = False
        self.context: Context = Context()
        self.terminal = self.context

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
            self._should_exit = True

    def pop_to_first_screen(self):
        while len(self._stack) > 1:
            self.pop_screen()

    def get_initial_screen(self):
        raise NotImplementedError()

    def start(self):
        self.replace_screen(self.get_initial_screen())
        super().start()

    def quit(self):
        while self._stack:
            self.pop_screen(may_exit=True)

    def terminal_update(self):
        i = 0
        for j, screen in enumerate(self._stack):
            if screen.covers_screen:
                i = j

        for screen in self._stack[i:]:
            screen.terminal_update(screen == self._stack[-1])

        return not self._should_exit

    def terminal_read(self, char):
        if self._stack:
            return self.active_screen.terminal_read(char)
