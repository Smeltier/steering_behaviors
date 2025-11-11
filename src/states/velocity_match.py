import pygame

from src.states.single_target_state import SingleTargetState
from src.outputs.steering_output import SteeringOutput

class VelocityMatch (SingleTargetState):

    def __init__(self, entity, target, max_acceleration=1, time_to_target=0.001):
        super().__init__(entity, target)
        self.time_to_target = time_to_target
        self.max_acceleration = max_acceleration

    def enter(self) -> None:
        print(f"[DEBUG] {self.entity.ID} -> VelocityMatch")
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
            steering.linear = self.target.velocity - self.entity.velocity
            steering.linear /= self.time_to_target

            if steering.linear.length() > self.max_acceleration:
                steering.linear.scale_to_length(self.max_acceleration)

            steering.angular = 0.0
            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering VelocityMatch (Atributo faltando): {e}")
            return steering
        
        except ZeroDivisionError:
            print(f"[ERROR] Divisão por zero no VelocityMatch (time_to_target=0).")
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no VelocityMatch: {e}")
            return steering