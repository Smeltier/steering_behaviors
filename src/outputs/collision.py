import pygame

class Collision:

    _position: pygame.Vector2
    _normal: pygame.Vector2

    def __init__(self):
        self._position = pygame.Vector2()
        self._normal = pygame.Vector2()

    @property
    def position(self) -> pygame.Vector2:
        return self.position
    
    @position.setter
    def position(self, value: pygame.Vector2) -> None:
        self._position = value

    @property
    def normal(self) -> pygame.Vector2:
        return self._normal
    
    @normal.setter
    def normal(self, value: pygame.Vector2) -> None:
        self._normal = value