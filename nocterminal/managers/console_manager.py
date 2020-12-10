from __future__ import annotations
import typing
import tcod

import assets

if typing.TYPE_CHECKING:
    from tcod.context import Context
    from .game_manager import GameManager


class ConsoleManager:
    
    def __init__(self, game_manager: GameManager) -> None:
        self.console_width = 110
        self.console_height = 55
        self.console_config = {
            'columns': self.console_width,
            'rows': self.console_height,
            'tileset': tcod.tileset.load_truetype_font(
                "./assets/simulacra.ttf", 16, 16),
            'title': "Simulacra",
            'vsync': True
        }
        self._context = tcod.context.new_terminal(**self.console_config)
        self._root_console = tcod.Console(self.console_width, 
                                          self.console_height)
    
    @property
    def context(self):
        return self._context
    
    @property
    def root_console(self):
        return self._root_console