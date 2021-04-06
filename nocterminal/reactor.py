from __future__ import annotations
from typing import *
from collections import deque

import ecstremity as ecs


if TYPE_CHECKING:
    from nocterminal.core_loop import CoreLoop


class Actor(ecs.Component):

    def __init__(self) -> None:
        self._energy: int = 0

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def has_energy(self) -> bool:
        return self._energy >= 0

    def add_energy(self, value: int) -> None:
        self._energy += value
        if self._energy >= 0:
            self._energy = 0

    def reduce_energy(self, value: int):
        self.add_energy(value * -1)

    def __lt__(self, other: Actor) -> bool:
        return self._energy < other._energy

    def __str__(self) -> str:
        return f"{self._energy}"

#
# class Reactor(BaseSystem):
#
#     def __init__(self, core: CoreLoop):
#         super().__init__(core)
#         self._query = self.core.engine.create_query(all_of=[ 'Actor' ])
#
#     def update(self):
#         entities = self._query.result
#         entities = deque(sorted(entities, key=lambda e: e['Actor']))
#
#         entity = entities.popleft()
#
#         if entity and not entity['Actor'].has_energy:
#             self.game.clock.increment(-1 * entity['Actor'].energy)
#             for entity in entities:
#                 entity['Actor'].add_energy(self.game.clock.tick_delta)
#
#         while entity and entity['Actor'].has_energy:
#             if entity.has('IsPlayer'):
#                 try:
#                     action = self.game.player.get_next_action()
#                     if action:
#                         action.act()
#                         return True
#                     continue
#                 except IndexError:
#                     return False
#
#             entity.fire_event('take_action')
#             entity = entities.popleft()
#
#         return False
