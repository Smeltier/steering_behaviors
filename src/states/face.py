import math
import pygame

from src.states.align import Align
from src.outputs.steering_output import SteeringOutput
from src.extra.steering_target import SteeringTarget

class Face (Align):

    def __init__(self, entity, target, slow_radius=50.0, target_radius=2.0, time_to_target=0.001, max_rotation=50.0, max_angular_acceleration=1000.0):
        super().__init__(entity, target, slow_radius, target_radius, time_to_target, max_rotation, max_angular_acceleration)

    def enter(self):
        print(f"[DEBUG] {self.entity.ID} -> Face")
        self.entity.change_color("white")

    def exit(self) -> None:
        return super().exit()    

    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        try:
            direction = self.target.position - self.entity.position

            if direction.length() == 0: return SteeringOutput()
            
            old_target = self.target

            temporary_target = SteeringTarget(
                position    = self.target.position,
                orientation = math.atan2(-direction.x, direction.y)
            )

            self.target = temporary_target
            steering = super().get_steering()
            self.target = old_target

            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Face (Atributo faltando): {e}")
            return SteeringOutput()
        
        except Exception as e:
            print(f"[ERROR] Erro inesperado no Face.get_steering: {e}")
            return SteeringOutput()