import pygame

class SteeringOutput:

    _linear: pygame.Vector2
    _angular: float

    def __init__(self) -> None:
        self._linear  = pygame.Vector2((0, 0))
        self._angular = 0.0

    @property
    def linear(self) -> pygame.Vector2:
        return self._linear
    
    @linear.setter
    def linear(self, new_linear: pygame.Vector2) -> None:
        self._linear = new_linear

    @property
    def angular(self) -> float:
        return self._angular
    
    @angular.setter
    def angular(self, new_angular: float) -> None:
        self._angular = new_angular