import math

import pygame

from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.states.single_target_state import SingleTargetState

class Align(SingleTargetState):

    _slow_radius: float
    _max_rotation: float
    _target_radius: float
    _time_to_target: float
    _max_angular_acceleration: float

    def __init__(self, entity: MovingEntity, target: MovingEntity, slow_radius: float, target_radius: float, time_to_target: float, max_rotation: float, max_angular_acceleration: float):
        super().__init__(entity, target)

        if time_to_target <= 0:
            raise ValueError("time_to_target não pode ser zero ou negativo.")
        if slow_radius < target_radius:
            raise ValueError("slow_radius não pode ser menor que target_radius.")
        
        self._slow_radius = slow_radius
        self._target_radius = target_radius
        self._time_to_target = time_to_target
        self._max_rotation = max_rotation
        self._max_angular_acceleration = max_angular_acceleration

    def enter(self) -> None:
        print(f"[DEBUG] {self._entity.ID} -> Align")
        self._entity.change_color("white")

    def exit(self) -> None:
        pass
    
    def execute(self, delta_time: float) -> None:
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self._target: return steering

        try:
            rotation = self._target.orientation - self._entity.orientation
            rotation = map_to_range(rotation)
            rotation_size = abs(rotation)

            if rotation_size < self._target_radius:
                return SteeringOutput()
            
            if rotation_size > self._slow_radius:
                target_rotation = self._max_rotation
            else:
                target_rotation = self._max_rotation * rotation_size / self._slow_radius

            target_rotation *= rotation / rotation_size

            steering.angular = target_rotation - self._entity.rotation
            steering.angular /= self._time_to_target

            angular_acceleration = abs(steering.angular)
            if angular_acceleration > self._max_angular_acceleration:
                steering.angular /= angular_acceleration
                steering.angular *= self._max_angular_acceleration

            steering.linear = pygame.math.Vector2(0,0)
            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Align (Atributo faltando): {e}")
            return steering
        
        except ZeroDivisionError as e:
            print(f"[ERROR] Divisão por zero no Align.get_steering: {e}")
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no Align.get_steering: {e}")
            return steering
        
def map_to_range(rotation):
    """ Normaliza um ângulo para o intervalo [-pi, +pi] """
    return (rotation + math.pi) % (2 * math.pi) - math.pi