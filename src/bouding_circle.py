import math
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.entities.moving_entity import MovingEntity

class BoundingCircle:

    _owner: 'MovingEntity'
    _radius: float

    def __init__(self, owner: 'MovingEntity', radius: float) -> None:
        self._owner = owner
        self._radius = radius
    
    @property
    def center(self) -> pygame.Vector2:
        return self._owner.position
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError("O raio do círculo não pode ser menor ou igual a zero.")
        self._radius = value