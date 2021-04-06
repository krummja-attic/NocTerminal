"""
The :py:mod:`~nocterminal.core_loop` module is responsible for running and coordinating
all of the sub-modules that make up NocTerminal as a comprehensive ASCII game engine.

The individual sub-modules may be extended directly, but the CoreLoop is a convenience
class that provides a minimal (though opinionated) boilerplate for game development.
"""
from __future__ import annotations
import nocterminal as noc


class CoreLoop:

    def __init__(self) -> None:
        self.terminal = noc.terminal

    def start(self):
        self.terminal.setup()
        self.loop()
        self.terminal.teardown()

    def terminal_update(self) -> bool:
        return True

    def terminal_read(self, char):
        pass

    def loop(self) -> None:
        # Update the active control context
        try:
            iteration = False
            while self.loop_iteration():
                iteration = True
                self.terminal.refresh()
            if not iteration:
                print("Exited after a single cycle.")
        except KeyboardInterrupt:
            pass

    def loop_iteration(self) -> bool:
        key = self.terminal.read()
        self.terminal_read(key)

        should_continue = self.terminal_update()
        # self.terminal.refresh()
        return should_continue
