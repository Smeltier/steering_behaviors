from abc import abstractmethod

import pygame

from src.states.state import State
from src.entities.moving_entity import MovingEntity

class SingleTargetState(State):

    _target: MovingEntity

    def __init__(self, entity: MovingEntity, target: MovingEntity):
        super().__init__(entity)

        if not target:
            raise ValueError('O alvo (target) não pode ser None.')
        
        self._target = target