from __future__ import annotations
from typing import Callable, Dict, Optional, TYPE_CHECKING

import tcod

from scene import Scene
from managers import Subject

if TYPE_CHECKING:
    from managers import T, CommandSet
    from managers.game_manager import GameManager
    from managers.action_manager import ActionManager
    from managers.console_manager import ConsoleManager
    from managers.input_manager import InputManager
    

class TestScene(Scene):
    
    def __init__(self, console_manager, scene_manager):
        super().__init__(console_manager, scene_manager)
        
    def render(self):
        console = self.console_manager.root_console
        console.print(2, 2, "Hello, world!")
    
    def cmd_confirm(self):
        self.scene_manager.transition("test2")
            
    @property
    def commands(self) -> CommandSet:
        return {
            tcod.event.K_RETURN: "confirm"
            }
           
            
class Test2Scene(Scene):
    
    def __init__(self, console_manager, scene_manager):
        super().__init__(console_manager, scene_manager)
        
    def render(self):
        console = self.console_manager.root_console
        console.print(10, 2, "Hello, world!")
    
    def cmd_confirm(self):
        self.scene_manager.transition("test1")
    
    @property
    def commands(self) -> CommandSet:
        return {
            tcod.event.K_RETURN: "confirm"
            }


class SceneManager(Subject):
    
    def __init__(self, game_manager: GameManager) -> None:
        super().__init__()
        self._current_scene: Optional[Scene] = None
        
        self._console_manager = game_manager.console_manager
        self._input_manager = game_manager.input_manager
        self.attach(self._input_manager)
        self._action_manager = game_manager.action_manager
        
        self.scenes: Dict[str, Scene] = {
            'test1': TestScene,
            'test2': Test2Scene
            }
        self.transition('test1')
    
    @property
    def current_scene(self) -> Scene:
        return self._current_scene
    
    def transition(self, scene: str) -> None:
        self._current_scene = self.scenes[scene](self._console_manager, self)
        self.notify()
    
    def render_scene(self, **kwargs):
        self._console_manager.root_console.clear()
        self.current_scene.render(**kwargs)
        
    def handle_input(self):
        self._input_manager.handle_input()
