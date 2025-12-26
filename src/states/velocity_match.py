import math
import pygame

from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.states.multi_target_steering import MultiTargetState

class VelocityMatch(MultiTargetState):

    _threshold: float
    _slow_radius: float
    _time_to_target: float

    def __init__(self, entity: MovingEntity, threshold: float = 10.0, slow_radius: float = 0.25, time_to_target: float = 0.1):
        super().__init__(entity, threshold)
        
        self._threshold = threshold  
        self._slow_radius = slow_radius  
        self._time_to_target = time_to_target  

    def enter(self) -> None:
        print(f"[DEBUG] {self._entity.ID} -> Alignment")
        self._entity.change_color("white")

    def exit(self) -> None:
        return super().exit()

    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()
        
        if not self._targets: 
            return steering

        sum_velocity = pygame.Vector2()
        count = 0

        for target in self._targets:
            if target == self._entity:
                continue

            distance = (target.position - self._entity.position).length()

            if distance > self._threshold:
                continue

            sum_velocity += target.velocity
            count += 1

        if count == 0: 
            return steering

        average_velocity = sum_velocity / count
        
        if average_velocity.magnitude() == 0:
            return steering

        try:
            desired_velocity = average_velocity.normalize() * self._entity.max_speed
        except ValueError:
             return steering

        steering.linear = desired_velocity - self._entity.velocity
        
        if steering.linear.magnitude() > self._entity.max_acceleration:
             steering.linear = steering.linear.normalize() * self._entity.max_acceleration

        return steering

def map_to_range(rotation):
    """ Normaliza o ângulo para o intervalo [-pi, +pi]. """
    return (rotation + math.pi) - (math.floor((rotation + math.pi) / (2 * math.pi)) * (2 * math.pi)) - math.pi