import math
import pygame

from src.states.single_target_state import SingleTargetState
from src.outputs.steering_output import SteeringOutput

class Align (SingleTargetState):

    def __init__(self, entity, target, slow_radius=50, target_radius=2.0, time_to_target=0.001, max_rotation=50, max_angular_acceleration=1000):
        super().__init__(entity, target)

        if time_to_target <= 0:
            raise ValueError("time_to_target não pode ser zero ou negativo.")
        if slow_radius < target_radius:
            raise ValueError("slow_radius não pode ser menor que target_radius.")
        
        self.slow_radius = slow_radius
        self.target_radius = target_radius
        self.time_to_target = time_to_target
        self.max_rotation = max_rotation
        self.max_angular_acceleration = max_angular_acceleration

    def enter(self) -> None:
        print(f"[DEBUG] {self.entity.ID} -> Align")
        self.entity.change_color("white")

    def exit(self) -> None:
        return super().exit()
    
    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)

    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self.target: return steering

        try:
            rotation = self.target.orientation - self.entity.orientation
            rotation = map_to_range(rotation)
            rotation_size = abs(rotation)

            if rotation_size < self.target_radius:
                return SteeringOutput()
            
            if rotation_size > self.slow_radius:
                target_rotation = self.max_rotation
            else:
                target_rotation = self.max_rotation * rotation_size / self.slow_radius

            target_rotation *= rotation / rotation_size

            steering.angular = target_rotation - self.entity.rotation
            steering.angular /= self.time_to_target

            angular_acceleration = abs(steering.angular)
            if angular_acceleration > self.max_angular_acceleration:
                steering.angular /= angular_acceleration
                steering.angular *= self.max_angular_acceleration

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