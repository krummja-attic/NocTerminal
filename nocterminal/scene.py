from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod, ABCMeta

from managers import CommandSet

if TYPE_CHECKING:
    from managers.console_manager import ConsoleManager
    from managers.scene_manager import SceneManager


class Scene(metaclass=ABCMeta):
    
    def __init__(
            self,
            console_manager: ConsoleManager,
            scene_manager: SceneManager
        ) -> None:
        self.console_manager = console_manager
        self.scene_manager = scene_manager
    
    @abstractmethod
    def render(self) -> None:
        pass
    
    # @abstractmethod
    # def handle_input(self) -> None:
    #     pass
    
    @property
    def commands(self) -> CommandSet:
        pass