from __future__ import annotations
from bearlibterminal import terminal as _terminal


class TerminalState:
    pass


for constant_key in (c for c in dir(_terminal) if c.startswith('TK_')):
    def getter(k):
        constant_value = getattr(_terminal, k)

        def get(self):
            return _terminal.state(constant_value)
        return get

    constant_name = constant_key[3:].lower()
    attr_name = f"num_{constant_name}" if constant_name[0].isdigit() else constant_name
    setattr(TerminalState, attr_name, property(getter(constant_key)))

terminal_state = TerminalState()
