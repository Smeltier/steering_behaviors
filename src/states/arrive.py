import math
from src.states.state import State
from src.outputs.steering_output import SteeringOutput

class Arrive (State):
    def __init__(self, entity, target, slow_radius=100, target_radius=10, time_to_target=0.1):
        super().__init__(entity)
        self.target = target
        self.slow_radius = slow_radius
        self.target_radius = target_radius
        self.time_to_target = time_to_target

    def enter(self) -> None:
        print(f"[DEBUG] {self.entity.ID} -> Arrive")
        self.entity.change_color("blue")

    def exit(self) -> None:
        return super().exit()

    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self.target:
            return steering
            
        self.direction = self.target.position - self.entity.position
        self.distance = self.direction.length()

        if self.distance < self.target_radius:
            return SteeringOutput()
        
        if self.distance > self.slow_radius:
            target_speed = self.entity.max_speed
        else:
            target_speed = self.entity.max_speed * self.distance / self.slow_radius

        target_velocity = self.direction.normalize()
        target_velocity *= target_speed

        steering.linear = target_velocity - self.entity.velocity
        steering.linear /= self.time_to_target 

        if steering.linear.length() > self.entity.max_acceleration:
            steering.linear.scale_to_length(self.entity.max_acceleration)

        steering.angular = 0
        return steering