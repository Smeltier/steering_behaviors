import pygame

from src.outputs.steering_output import SteeringOutput
from src.states.state import State

class Flee (State):

    def __init__(self, entity, target):
        super().__init__(entity)
        self.target = target

    def execute(self, delta_time):
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target: return steering

        direction = self.entity.position - self.target.position

        if direction.length_squared() == 0:
            return steering

        direction.normalize_ip()
        steering.linear = direction * self.entity.max_acceleration
        steering.angular = 0

        return steering

    def enter(self):
        print(f"[DEBUG] {self.entity.ID} -> Flee")
        self.entity.change_color("yellow")

    def exit(self):
        pass