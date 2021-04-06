from __future__ import annotations
from bearlibterminal import terminal as _terminal
from morphism import *


class BaseTerminal:

    def __getattr__(self, k):
        return getattr(_terminal, k)

    def setup(self, composition: bool = True, bkcolor: int = 0xFF151515) -> None:
        _terminal.open()
        _terminal.composition(composition)
        _terminal.bkcolor(bkcolor)

    @staticmethod
    def teardown() -> None:
        _terminal.composition(False)
        _terminal.close()

    @staticmethod
    def refresh():
        _terminal.refresh()

    @staticmethod
    def clear(bkcolor: int = 0xFF151515):
        _terminal.clear()
        _terminal.bkcolor(bkcolor)

    @staticmethod
    def has_input():
        return _terminal.has_input()

    # Clear Area =========================================================================
    @staticmethod
    def clear_area( *args ) -> None:
        if args and isinstance(args[0], Rect):
            rect: Rect = args[0]
            return _terminal.clear_area(
                rect.origin.x, rect.origin.y,
                rect.size.width, rect.size.height
                )
        return _terminal.clear_area(*args)

    # Crop ===============================================================================
    @staticmethod
    def crop( *args ):
        if args and isinstance(args[0], Rect):
            return _terminal.crop(
                args[0].origin.x, args[0].origin.y,
                args[0].size.width, args[0].size.height)
        else:
            return _terminal.crop(*args)

    # Puts ===============================================================================
    @staticmethod
    def puts(*args):
        if args and isinstance(args[0], Point):
            # if args[2] and isinstance(args[2], Size):
            #     return _terminal.puts(args[0].x, args[0].y, args[1],
            #                          args[2].width, args[2].height, *args[3:])
            return _terminal.puts(args[0].x, args[0].y, *args[1:])
        else:
            return _terminal.puts(*args)

    # Printf =============================================================================
    @staticmethod
    def printf(*args):
        if isinstance(args[0], Point):
            return _terminal.printf(args[0].x, args[0].y, *args[1:])
        else:
            return _terminal.printf(*args)

    # Put ================================================================================
    @staticmethod
    def put(*args):
        if isinstance(args[0], Point):
            return _terminal.put(args[0].x, args[0].y, *args[1:])
        else:
            return _terminal.put(*args)

    # Pick ===============================================================================
    @staticmethod
    def pick(*args):
        if isinstance(args[0], Point):
            return _terminal.pick(args[0].x, args[0].y, *args[1:])
        else:
            return _terminal.pick(*args)

    # Pick Color =========================================================================
    @staticmethod
    def pick_color(*args):
        if isinstance(args[0], Point):
            return _terminal.pick_color(args[0].x, args[0].y, *args[1:])
        else:
            return _terminal.pick_color(*args)

    # Pick Bkcolor =======================================================================
    @staticmethod
    def pick_bkcolor(*args):
        if isinstance(args[0], Point):
            return _terminal.pick_bkcolor(args[0].x, args[0].y, *args[1:])
        else:
            return _terminal.pick_bkcolor(*args)

    # Put Ext ============================================================================
    @staticmethod
    def put_ext(*args):
        if isinstance(args[0], Point):
            return _terminal.put_ext(args[0].x, args[0].y, args[1].x, args[1].y, *args[2:])
        else:
            return _terminal.put_ext(*args)

    # Read Str ===========================================================================
    @staticmethod
    def read_str(*args):
        if isinstance(args[0], Point):
            return _terminal.read_str(args[0].x, args[0].y, *args[1:])
        else:
            return _terminal.read_str(*args)


terminal = BaseTerminal()

