from abc import abstractmethod

from src.outputs.steering_output import SteeringOutput

class State ():

    def __init__(self, entity):
        self.entity = entity

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