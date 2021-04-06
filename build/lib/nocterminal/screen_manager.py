from nocterminal.ui import Screen
from nocterminal.blt import Context, CoreLoop
from typing import *


class ScreenManager(CoreLoop):

    def __init__(self) -> None:
        super().__init__()
        self.should_exit = False
        self.ctx = Context()
        self._stack: List[Screen] = []

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
        screen.manager = self
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
            self.should_exit = True

    def pop_to_first_screen(self):
        while len(self._stack) > 1:
            self.pop_screen()

    def quit(self):
        while self._stack:
            self.pop_screen(may_exit=True)

    @staticmethod
    def get_initial_screen():
        raise NotImplementedError()

    def update(self):
        if self.ctx.has_input():
            char = self.ctx.terminal.read()
            self.terminal_read(char)
        self.ctx.clear()
        should_continue = self.terminal_update()
        return should_continue

    def terminal_update(self):
        i = 0
        for j, screen in enumerate(self._stack):
            if screen.covers_screen:
                i = j
        for screen in self._stack[i:]:
            screen.terminal_update(screen == self._stack[-1])
        return not self.should_exit

    def terminal_read(self, char):
        if self._stack:
            return self.active_screen.terminal_read(char)
