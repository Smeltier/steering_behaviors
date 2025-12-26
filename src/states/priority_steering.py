import pygame

from src.states.state import State
from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.states.blended_steering import BlendedSteering

class PrioritySteering (State):

    _groups: list[BlendedSteering]
    _epsilon: float

    def __init__(self, entity: MovingEntity, groups: list[BlendedSteering] | None = None, epsilon: float = 0.1):
        super().__init__(entity)
        self._groups = groups or []
        self._epsilon = epsilon

    def enter(self):
        print(f"[DEBUG] {self._entity.ID} -> PrioritySteering")
        self._entity.change_color("white")
    
    def exit(self):
        pass
    
    def execute(self, delta_time):
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        for group in self._groups:
            steering = group.get_steering()

            if steering.linear.length() > self._epsilon or abs(steering.angular) > self.epsilon:
                return steering
            
        return SteeringOutput()