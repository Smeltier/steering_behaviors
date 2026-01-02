from abc import abstractmethod

import pygame

from src.states.state import State
from src.entities.moving_entity import MovingEntity

class MultiTargetState(State):

    _targets: list[MovingEntity]
    _threshold: float

    def __init__(self, entity: MovingEntity, threshold: float = 100.0) -> None:
        super().__init__(entity)

        if threshold <= 0.0:
            raise ValueError('threshold deve ser maior que zero.')

        self._targets = self._entity._environment._entities
        self._threshold = threshold

    @property
    def threshold(self) -> float:
        return self._threshold
    
    @threshold.setter
    def threshold(self, value: float) -> None:
        self._threshold = value