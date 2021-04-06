"""
The :py:mod:`~nocterminal.core_loop` module is responsible for running and coordinating
all of the sub-modules that make up NocTerminal as a comprehensive ASCII game engine.

The individual sub-modules may be extended directly, but the CoreLoop is a convenience
class that provides a minimal (though opinionated) boilerplate for game development.
"""

import nocterminal as noc
import functools


def calltracker(func):
    @functools.wraps(func)
    def wrapper(*args):
        wrapper.has_been_called = True
        return func(*args)
    wrapper.has_been_called = False
    return wrapper


class CoreLoop:
    """
    A game loop that manages the sub-modules that comprise NocTerminal.

    This class must be inherited, with certain of its methods (documented below)
    given concrete implementations. **Read this documentation carefully** to ensure
    that no issues arise in using this class!

    :py:meth:`~CoreLoop.systems_init` is a hook for adding in custom ECS systems.

    .. py:attribute:: terminal

       Instance of :py:class:`~nocterminal.blt.base_terminal.BaseTerminal`, AKA the actual NocTerminal object.

    .. py:attribute:: director

       Screen and context manager.

    .. py:attribute:: commander

       Input management.

    .. py:attribute:: reactor

       Actor event system - based on ECStremity.
    """

    def __init__(self) -> None:
        self.engine = None
        self.engine_init()
        self.systems_init()

        self.terminal = noc.terminal
        self.director = noc.Director(core=self)
        self.commander = noc.Commander(core=self)
        self.reactor = noc.Reactor(core=self)

    def engine_init(self):
        self.engine = noc.Engine(client=self)

    def systems_init(self):
        """Override this method to provide additional systems to the core loop."""
        raise NotImplementedError("Without systems, nothing fun will happen!")

    def start(self):
        """Sets up the terminal, calls the :py:meth:`~Director.get_initial_screen` hook, and
        fires up the game loop. On exit, tears down the terminal.
        """
        self.terminal.setup()
        self.director.replace_screen(self.get_initial_screen())
        self.loop()
        self.terminal.teardown()

    def get_initial_screen(self):
        """Hook to load the start screen.

        .. warning:: This method *must* be overridden with a valid :py:class:`~nocterminal.ui.screen.Screen` object.
        """
        raise NotImplementedError("No initial screen - nothing to display!")

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
        """Single cycle of the game loop.

        .. warning:: This method *must* return True, or the loop will exit.
        """
        should_continue = self.director.update()
        return should_continue

    def engine_update(self) -> None:
        """Update the engine, allowing the actor event system to loop once. Running this
        iterates a "turn" of the game.

        .. warning:: This method must be called in the main game screen instance. See examples for implementation details.
        """
        actor_cycle = self.reactor.update()
        if actor_cycle:
            self.systems_update()

    def systems_update(self):
        raise NotImplementedError("Provide concrete systems to iterate during "
                                  "the core loop.")
