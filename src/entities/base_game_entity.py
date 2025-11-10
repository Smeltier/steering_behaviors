import pygame

from abc import abstractmethod

class BaseGameEntity ():
    _next_ID = 1000

    def __init__(self, x, y, world):
        self.ID = self._set_ID()
        self.position: pygame.Vector2 = pygame.Vector2((x, y))
        self.environment = world

    def _set_ID(self) -> int:
        entity_ID = BaseGameEntity._next_ID
        BaseGameEntity._next_ID += 1
        return entity_ID
    
    @abstractmethod
    def update(self, delta_time) -> None:
        pass