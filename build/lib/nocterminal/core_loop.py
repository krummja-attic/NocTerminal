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
        self.terminal.setup()
        self.director.replace_screen(self.get_initial_screen())
        self.loop()
        self.terminal.teardown()

    def get_initial_screen(self):
        raise NotImplementedError("No initial screen - nothing to display!")

    def loop(self):
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

    def loop_iteration(self):
        should_continue = self.director.update()
        return should_continue

    @calltracker
    def engine_update(self):
        """This method must be called in the main game screen instance."""
        actor_cycle = self.reactor.update()
        if actor_cycle:
            self.systems_update()

    def systems_update(self):
        raise NotImplementedError("Provide concrete systems to iterate during "
                                  "the core loop.")
