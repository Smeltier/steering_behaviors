import pygame

from abc import abstractmethod

from src.states.state import State
from src.outputs.steering_output import SteeringOutput

class SingleTargetState (State):

    def __init__(self, entity, target):
        super().__init__(entity)

        if not target:
            raise ValueError('O alvo (target) não pode ser None.')
        
        self.target = target

    @abstractmethod
    def enter(self) -> None: 
        pass

    @abstractmethod
    def exit(self) -> None: 
        pass

    @abstractmethod
    def execute(self, delta_time) -> None: 
        pass

    @abstractmethod
    def get_steering(self) -> SteeringOutput:
        pass