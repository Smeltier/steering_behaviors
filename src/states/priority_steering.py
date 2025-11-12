import pygame

from src.states.state import State
from src.states.blended_steering import BlendedSteering
from src.outputs.steering_output import SteeringOutput

class PrioritySteering (State):

    def __init__(self, entity, groups: list[BlendedSteering] | None = None):
        super().__init__(entity)
        self.groups = groups or []
        self.epsilon = 0.1

    def enter(self):
        print(f"[DEBUG] {self.entity.ID} -> PrioritySteering")
        self.entity.change_color("white")
    
    def exit(self):
        return super().exit()
    
    def execute(self, delta_time):
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        for group in self.groups:
            steering = group.get_steering()

            if steering.linear.length() > self.epsilon or abs(steering.angular) > self.epsilon:
                return steering
            
        return SteeringOutput()