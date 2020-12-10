from __future__ import annotations

import tcod

from .console_manager import ConsoleManager
from .scene_manager import SceneManager
from .input_manager import InputManager
from .action_manager import ActionManager


class GameManager:

    def __init__(self) -> None:
        self.console_manager = ConsoleManager(self)
        self.root_console = self.console_manager.root_console

        self.input_manager = InputManager(self)
        self.action_manager = ActionManager(self)
        self.scene_manager = SceneManager(self)

    def loop(self):
        while True:
            self.console_manager.context.present(self.root_console)
            self.scene_manager.render_scene()
            self.scene_manager.handle_input()
