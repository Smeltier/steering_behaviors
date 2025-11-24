import pygame

from abc import abstractmethod

from src.states.state import State
from src.outputs.steering_output import SteeringOutput

class MultiTargetSteering (State):

    def __init__ (self, entity, threshold=100.0) -> None:
        super().__init__(entity)

        if threshold <= 0.0:
            raise ValueError('threshold deve ser maior que zero.')

        self.targets = self.entity.environment.entities
        self.threshold = threshold