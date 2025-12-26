import math

import pygame

from src.states.align import Align
from src.entities.moving_entity import MovingEntity
from src.extra.steering_target import SteeringTarget
from src.outputs.steering_output import SteeringOutput

class Face (Align):

    def __init__(self, entity: MovingEntity, target: MovingEntity, slow_radius: float = 50.0, target_radius: float = 2.0, time_to_target: float = 0.001, max_rotation: float = 50.0, max_angular_acceleration: float = 1000.0):
        super().__init__(entity, target, slow_radius, target_radius, time_to_target, max_rotation, max_angular_acceleration)

    def enter(self):
        print(f"[DEBUG] {self._entity.ID} -> Face")
        self._entity.change_color("white")

    def exit(self) -> None:
        return super().exit()    

    def execute(self, delta_time: float) -> None:
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        try:
            direction = self._target.position - self._entity.position

            if direction.length() == 0: return SteeringOutput()
            
            old_target = self._target

            temporary_target = SteeringTarget(
                position    = self._target.position,
                orientation = math.atan2(-direction.x, direction.y)
            )

            self._target = temporary_target
            steering = super().get_steering()
            self._target = old_target

            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Face (Atributo faltando): {e}")
            return SteeringOutput()
        
        except Exception as e:
            print(f"[ERROR] Erro inesperado no Face.get_steering: {e}")
            return SteeringOutput()