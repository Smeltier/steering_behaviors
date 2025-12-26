import pygame

class SteeringTarget:

    _position: pygame.Vector2
    _velocity: pygame.Vector2
    _orientation: float
    _rotation: float

    def __init__(self, position: pygame.Vector2, orientation: float = 0.0):
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.orientation = orientation
        self.rotation = 0 

    @property
    def position(self) -> pygame.Vector2:
        return self._position
    
    @position.setter
    def position(self, value: pygame.Vector2) -> None:
        self._position = value

    @property
    def velocity(self) -> pygame.Vector2:
        return self._velocity
    
    @velocity.setter
    def velocity(self, value: pygame.Vector2) -> None:
        self._velocity = value

    @property
    def orientation(self) -> float:
        return self._orientation
    
    @orientation.setter
    def orientation(self, value: float) -> None:
        self._orientation = value
    
    @property
    def rotation(self) -> float:
        return self._rotation
    
    @orientation.setter
    def rotation(self, value: float) -> None:
        self._rotation = value