import math
import random
import pygame

from src.states.face import Face
from src.outputs.steering_output import SteeringOutput
from src.extra.steering_target import SteeringTarget

class Wander (Face):
    def __init__(self, entity, target, slow_radius=50, target_radius=2, time_to_target=0.001,
                 max_rotation=50, max_angular_acceleration=1000, wander_offset=20, wander_radius=50,
                 wander_rate=1.0, max_acceleration=100):
        super().__init__(entity, target, slow_radius, target_radius, 
                         time_to_target, max_rotation, max_angular_acceleration)

        self.wander_offset = wander_offset
        self.wander_radius = wander_radius
        self.wander_rate = wander_rate
        self.max_acceleration = max_acceleration
        self.wander_orientation = 0.0

    def enter(self):
        print(f"[DEBUG] {self.entity.ID} -> Wander")
        self.entity.change_color("pink")
    
    def exit(self) -> None:
        return super().exit()
    
    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        try:
            self.wander_orientation += random.uniform(-1.0, 1.0) * self.wander_rate

            target_orientation = self.wander_orientation + self.entity.orientation

            orientation_vector = pygame.math.Vector2(math.cos(self.entity.orientation), math.sin(self.entity.orientation))
            target_orientation_vector = pygame.math.Vector2(math.cos(target_orientation), math.sin(target_orientation))
            
            circle_center = self.entity.position + self.wander_offset * orientation_vector

            target_position = circle_center + self.wander_radius * target_orientation_vector

            old_target = self.target

            wander_target = SteeringTarget(target_position)
            wander_target.position = target_position

            self.target = wander_target
            steering = super().get_steering()
            self.target = old_target

            wander_force = orientation_vector * self.max_acceleration
            steering.linear += wander_force

            return steering
        

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Wander (Atributo faltando): {e}")
            return SteeringOutput()
        
        except Exception as e:
            print(f"[ERROR] Erro inesperado no Wander.get_steering: {e}")
            return SteeringOutput()
