from __future__ import annotations
from typing import TypeVar, Union, Dict, List, Protocol, Optional
from contextlib import suppress


T = TypeVar("T")
CommandSet = Union[Dict[int, str], Dict[int, int]]


class Observer(Protocol):
    def update(self, subject: Subject) -> None:
        pass


class Subject:
    
    def __init__(self) -> None:
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        with suppress(ValueError):
            self._observers.remove(observer)
    
    def notify(self, modifier: Optional[Observer] = None) -> None:
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)
