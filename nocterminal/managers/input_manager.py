from __future__ import annotations
from typing import (Callable, 
                    Generic, 
                    Dict, 
                    Optional, 
                    TypeVar, 
                    Union, 
                    TYPE_CHECKING)

import tcod
from tcod.event import EventDispatch
from managers import T, CommandSet

from managers import Observer

if TYPE_CHECKING:
    from scene import Scene
    from managers import Subject
    from managers.game_manager import GameManager
    from managers.scene_manager import SceneManager


class InputManager(Generic[T], EventDispatch[T], Observer):
    
    def __init__(self, game_manager: GameManager) -> None:
        super().__init__()
        self._scene_manager: SceneManager = None
        self._current_scene: Scene = None
    
    def update(self, subject: SceneManager):
        self._scene_manager = subject
        self._current_scene = subject.current_scene
    
    def handle_input(self) -> Callable[[], Optional[T]]:
        for event in tcod.event.get():
            value: Callable[[], Optional[T]] = self.dispatch(event)                
            if value is not None:
                return value

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if self._current_scene is not None:
            if event.sym in self._current_scene.commands:
                command: Callable[[], Optional[T]] = getattr(
                    self._current_scene, 
                    f"cmd_{self._current_scene.commands[event.sym]}"
                    )
                #! Route successful command to ActionManager
                command()
            #! Deal with failure messages
            return None
