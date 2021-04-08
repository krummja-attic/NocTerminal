"""
The :py:mod:`~nocterminal.core_loop` module is responsible for running and coordinating
all of the sub-modules that make up NocTerminal as a comprehensive ASCII game engine.

The individual sub-modules may be extended directly, but the CoreLoop is a convenience
class that provides a minimal (though opinionated) boilerplate for game development.
"""
from __future__ import annotations
import nocterminal as noc
import time


class CoreLoop:

    def __init__(self):
        self._last_update: float = 0.0

    def start(self):
        noc.terminal.setup()
        self.main_loop()
        noc.terminal.teardown()

    def main_loop(self) -> None:
        # Update the active control context
        try:
            iteration = False
            while self.loop_iteration():
                iteration = True
                noc.terminal.refresh()
            if not iteration:
                print("Exited after a single cycle.")
        except KeyboardInterrupt:
            pass

    def loop_iteration_hook(self):
        pass

    def loop_iteration(self) -> bool:
        now = time.time()
        dt = now - self._last_update
        should_continue = self.update(dt)
        self.loop_iteration_hook()
        self._last_update = now
        return should_continue

    def update(self, dt):
        return True

    def terminal_read(self, char):
        pass

    def terminal_update(self):
        pass
