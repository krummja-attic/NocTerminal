"""
The :py:mod:`~nocterminal.core_loop` module is responsible for running and coordinating
all of the sub-modules that make up NocTerminal as a comprehensive ASCII game engine.

The individual sub-modules may be extended directly, but the CoreLoop is a convenience
class that provides a minimal (though opinionated) boilerplate for game development.
"""
from __future__ import annotations
import nocterminal as noc


class CoreLoop:

    def start(self):
        noc.terminal.setup()
        self.loop()
        noc.terminal.teardown()

    def on_terminal_update(self):
        pass

    def update(self):
        return True

    def loop(self) -> None:
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

    def loop_iteration(self) -> bool:
        should_continue = self.update()
        return should_continue
