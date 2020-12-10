from __future__ import annotations
from typing import Callable, Optional, TYPE_CHECKING

from managers import T, CommandSet

if TYPE_CHECKING:
    from managers.game_manager import GameManager
    from managers.input_manager import InputManager


class Result:
    pass


class ActionManager:
    
    def __init__(self, game_manager: GameManager) -> None:
        pass
        
    def interpret_command(self, command: Callable[[], Optional[T]]) -> Result:
        pass