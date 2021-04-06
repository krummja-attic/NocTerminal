from __future__ import annotations
from ecstremity import EngineAdapter


class Engine(EngineAdapter):

    def __init__(self, client=None) -> None:
        super().__init__(client=client)
