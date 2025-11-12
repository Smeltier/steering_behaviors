import math
import pygame

from src.states.multi_target_steering import MultiTargetSteering
from src.outputs.steering_output import SteeringOutput

class VelocityMatch (MultiTargetSteering):

    def __init__(self, entity, threshold=10, slow_radius=0.25, time_to_target=0.1):
        super().__init__(entity, threshold)
        
        self.threshold = threshold  
        self.slow_radius = slow_radius  
        self.time_to_target = time_to_target  

    def enter(self) -> None:
        print(f"[DEBUG] {self.entity.ID} -> Alignment")
        self.entity.change_color("white")

    def exit(self) -> None:
        return super().exit()

    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()
        
        if not self.targets: 
            return steering

        sum_velocity = pygame.Vector2()
        count = 0

        for target in self.targets:
            if target == self.entity:
                continue

            distance = (target.position - self.entity.position).length()

            if distance > self.threshold:
                continue

            sum_velocity += target.velocity
            count += 1

        if count == 0: 
            return steering

        average_velocity = sum_velocity / count
        
        if average_velocity.magnitude() == 0:
            return steering

        try:
            desired_velocity = average_velocity.normalize() * self.entity.max_speed
        except ValueError:
             return steering

        steering.linear = desired_velocity - self.entity.velocity
        
        if steering.linear.magnitude() > self.entity.max_acceleration:
             steering.linear = steering.linear.normalize() * self.entity.max_acceleration

        return steering

def map_to_range(rotation):
    """ Normaliza o ângulo para o intervalo [-pi, +pi]. """
    return (rotation + math.pi) - (math.floor((rotation + math.pi) / (2 * math.pi)) * (2 * math.pi)) - math.pi