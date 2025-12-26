import pygame

from abc import abstractmethod

from src.world import World

class BaseGameEntity:

    _environment: World
    _position: pygame.Vector2
    _ID: int
    _next_ID: int = 1000

    def __init__(self, x: float, y: float, world: World) -> None:
        self._position = pygame.Vector2((x, y))
        self._environment = world
        self._ID = self._set_ID()

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """ Atualiza o estado da entidade. """
        pass

    @property
    def position(self) -> pygame.Vector2:
        return self._position
    
    @position.setter
    def position(self, new_position: pygame.Vector2) -> None:
        self._position = new_position

    def _set_ID(self) -> int:
        entity_ID = BaseGameEntity._next_ID
        BaseGameEntity._next_ID += 1
        return entity_ID