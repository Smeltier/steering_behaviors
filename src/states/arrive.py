import math

import pygame

from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.states.single_target_state import SingleTargetState

class Arrive (SingleTargetState):

    _distance: float
    _slow_radius: float
    _target_radius: float
    _time_to_target: float
    _direction: pygame.Vector2

    def __init__(self, entity: MovingEntity, target: MovingEntity, slow_radius: float = 100.0, target_radius: float = 10.0, time_to_target: float = 0.1):
        super().__init__(entity, target)

        if time_to_target <= 0:
            raise ValueError("time_to_target não pode ser zero ou negativo.")

        self._slow_radius = slow_radius
        self._target_radius = target_radius
        self._time_to_target = time_to_target

    def enter(self) -> None:
        print(f"[DEBUG] {self._entity.ID} -> Arrive")
        self._entity.change_color("blue")

    def exit(self) -> None:
        return super().exit()

    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self._target: return steering

        try:
            self._direction = self._target.position - self._entity.position
            self._distance = self._direction.length()

            if self._distance < self._target_radius:
                return SteeringOutput()
            
            if self._distance > self._slow_radius:
                target_speed = self._entity.max_speed
            else:
                target_speed = self._entity.max_speed * self._distance / self._slow_radius

            target_velocity = self._direction.normalize()
            target_velocity *= target_speed

            steering.linear = target_velocity - self._entity.velocity
            steering.linear /= self._time_to_target

            if steering._linear.length() > self._entity.max_acceleration:
                steering._linear.scale_to_length(self._entity.max_acceleration)

            steering.angular = 0
            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Arrive (Atributo faltando): {e}")
            return steering
        
        except ZeroDivisionError:
            print(f"[ERROR] time_to_target é zero no Arrive.get_steering!")
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no Arrive.get_steering: {e}")
            return steering